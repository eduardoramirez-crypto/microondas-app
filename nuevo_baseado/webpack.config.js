// Configuración de Webpack para desarrollo y producción
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = (env, argv) => {
    const isProduction = argv.mode === 'production';
    
    return {
        entry: {
            main: './src/main.js',
            security: './security.js'
        },
        
        output: {
            path: path.resolve(__dirname, 'dist'),
            filename: isProduction ? '[name].[contenthash].js' : '[name].js',
            clean: true,
            // No generar source maps en producción
            devtool: isProduction ? false : 'source-map'
        },
        
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env'],
                            plugins: isProduction ? [
                                // Ofuscación adicional en producción
                                ['transform-remove-console', { exclude: ['error', 'warn'] }]
                            ] : []
                        }
                    }
                },
                {
                    test: /\.css$/,
                    use: [
                        isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
                        'css-loader'
                    ]
                }
            ]
        },
        
        plugins: [
            new HtmlWebpackPlugin({
                template: './templates/ptpFangioactualizacion.html',
                filename: 'index.html',
                minify: isProduction ? {
                    removeComments: true,
                    collapseWhitespace: true,
                    removeRedundantAttributes: true,
                    useShortDoctype: true,
                    removeEmptyAttributes: true,
                    removeStyleLinkTypeAttributes: true,
                    keepClosingSlash: true,
                    minifyJS: true,
                    minifyCSS: true,
                    minifyURLs: true
                } : false
            }),
            
            ...(isProduction ? [
                new MiniCssExtractPlugin({
                    filename: '[name].[contenthash].css'
                })
            ] : [])
        ],
        
        optimization: {
            minimize: isProduction,
            minimizer: [
                new TerserPlugin({
                    terserOptions: {
                        compress: {
                            drop_console: true,
                            drop_debugger: true,
                            pure_funcs: ['console.log', 'console.info', 'console.debug']
                        },
                        mangle: {
                            toplevel: true,
                            properties: {
                                regex: /^_/
                            }
                        },
                        format: {
                            comments: false
                        }
                    },
                    extractComments: false
                }),
                
                ...(isProduction ? [new CssMinimizerPlugin()] : [])
            ],
            
            splitChunks: {
                chunks: 'all',
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'vendors',
                        chunks: 'all'
                    }
                }
            }
        },
        
        devServer: {
            static: {
                directory: path.join(__dirname, 'dist')
            },
            compress: true,
            port: 8080,
            hot: true,
            // Deshabilitar source maps en desarrollo para mayor seguridad
            devtool: false
        },
        
        // Configuración de seguridad
        resolve: {
            alias: {
                '@': path.resolve(__dirname, 'src')
            }
        },
        
        // Configuración de performance
        performance: {
            hints: isProduction ? 'warning' : false,
            maxEntrypointSize: 512000,
            maxAssetSize: 512000
        }
    };
};
