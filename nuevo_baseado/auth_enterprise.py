from flask import Blueprint, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps
from models_enterprise import db, User, Role, AuditLog
import json

# Blueprint para autenticación
auth_bp = Blueprint('auth', __name__)

# Login manager
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

def create_token(user_id):
    """Crear token JWT para el usuario"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    from config_enterprise import Config
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    """Decorator para proteger rutas con token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            from config_enterprise import Config
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def role_required(required_role):
    """Decorator para verificar roles específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            
            if current_user.role.name != required_role and current_user.role.name != 'admin':
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(permission):
    """Decorator para verificar permisos específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            
            if not current_user.has_permission(permission):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_audit(user_id, action, resource_type=None, resource_id=None, details=None):
    """Registrar actividad en el log de auditoría"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=json.dumps(details) if details else None,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging audit: {e}")

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuarios"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Crear sesión
        login_user(user, remember=True)
        
        # Crear token JWT
        token = create_token(user.id)
        
        # Log de auditoría
        log_audit(user.id, 'login', 'user', user.id, {
            'username': user.username,
            'ip_address': request.remote_addr
        })
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Endpoint para logout de usuarios"""
    user_id = current_user.id
    username = current_user.username
    
    logout_user()
    
    # Log de auditoría
    log_audit(user_id, 'logout', 'user', user_id, {
        'username': username,
        'ip_address': request.remote_addr
    })
    
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registro de usuarios (solo admin puede crear usuarios)"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Username, password and email are required'}), 400
    
    # Verificar si el usuario ya existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Obtener rol por defecto (user)
    default_role = Role.query.filter_by(name='user').first()
    if not default_role:
        return jsonify({'error': 'Default role not found'}), 500
    
    # Crear nuevo usuario
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        role_id=default_role.id
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Log de auditoría
        log_audit(user.id, 'register', 'user', user.id, {
            'username': user.username,
            'email': user.email
        })
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error creating user'}), 500

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Obtener perfil del usuario actual"""
    return jsonify({
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Actualizar perfil del usuario actual"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Campos permitidos para actualización
    allowed_fields = ['first_name', 'last_name', 'email']
    
    for field in allowed_fields:
        if field in data:
            setattr(current_user, field, data[field])
    
    try:
        db.session.commit()
        
        # Log de auditoría
        log_audit(current_user.id, 'update_profile', 'user', current_user.id, {
            'updated_fields': list(data.keys())
        })
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error updating profile'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Cambiar contraseña del usuario actual"""
    data = request.get_json()
    
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    if not current_user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    current_user.set_password(data['new_password'])
    
    try:
        db.session.commit()
        
        # Log de auditoría
        log_audit(current_user.id, 'change_password', 'user', current_user.id, {
            'password_changed': True
        })
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error changing password'}), 500

@auth_bp.route('/verify-token', methods=['POST'])
@token_required
def verify_token(current_user):
    """Verificar si un token es válido"""
    return jsonify({
        'valid': True,
        'user': current_user.to_dict()
    }), 200

def init_roles():
    """Inicializar roles por defecto"""
    roles_data = [
        {
            'name': 'admin',
            'description': 'Administrator with full access',
            'permissions': [
                'user_management', 'project_management', 'file_management',
                'audit_logs', 'system_settings', 'reports'
            ]
        },
        {
            'name': 'manager',
            'description': 'Project manager with project management access',
            'permissions': [
                'project_management', 'file_management', 'reports'
            ]
        },
        {
            'name': 'user',
            'description': 'Regular user with basic access',
            'permissions': [
                'project_creation', 'file_upload', 'project_view'
            ]
        }
    ]
    
    for role_data in roles_data:
        existing_role = Role.query.filter_by(name=role_data['name']).first()
        if not existing_role:
            role = Role(
                name=role_data['name'],
                description=role_data['description'],
                permissions=json.dumps(role_data['permissions'])
            )
            db.session.add(role)
    
    try:
        db.session.commit()
        print("Roles initialized successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing roles: {e}")

def create_admin_user():
    """Crear usuario administrador por defecto"""
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        print("Admin role not found. Please initialize roles first.")
        return
    
    existing_admin = User.query.filter_by(username='admin').first()
    if not existing_admin:
        admin_user = User(
            username='admin',
            email='admin@site-survey.com',
            first_name='System',
            last_name='Administrator',
            role_id=admin_role.id,
            is_active=True,
            is_verified=True
        )
        admin_user.set_password('admin123')  # Cambiar en producción
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully")
            print("Username: admin")
            print("Password: admin123")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")
    else:
        print("Admin user already exists") 