from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建蓝图
bp = Blueprint('ai', __name__, url_prefix='/api/ai')

# 大模型API配置
MODEL_CONFIGS = {
    'deepseek': {
        'url': os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions'),
        'api_key': os.getenv('DEEPSEEK_API_KEY', ''),
        'model': os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    },
    'qwen': {
        'url': os.getenv('QWEN_API_URL', 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'),
        'api_key': os.getenv('QWEN_API_KEY', ''),
        'model': os.getenv('QWEN_MODEL', 'qwen-turbo')
    },
    'doubao': {
        'url': os.getenv('DOUBAO_API_URL', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'),
        'api_key': os.getenv('DOUBAO_API_KEY', ''),
        'model': os.getenv('DOUBAO_MODEL', 'ep-20240214170345-5k2nw')
    }
}

# 生成文本
@bp.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    model_name = data.get('model', 'deepseek')
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 500)
    api_key = data.get('api_key', '')
    
    if not model_name or not prompt:
        return jsonify({'error': '缺少模型名称或提示词'}), 400
    
    # 获取模型配置
    model_config = MODEL_CONFIGS.get(model_name)
    if not model_config:
        return jsonify({'error': '不支持的模型'}), 400
    
    # 优先使用前端传递的API密钥，如果没有则使用环境变量中的
    if not api_key:
        api_key = model_config['api_key']
    
    if not api_key:
        return jsonify({'error': '未配置API密钥'}), 500
    
    try:
        # 根据模型类型调用不同的API
        if model_name == 'deepseek':
            print(f"调用DeepSeek API，URL: {model_config['url']}")
            print(f"Prompt长度: {len(prompt)} 字符")
            
            response = requests.post(
                model_config['url'],
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                },
                json={
                    'model': model_config['model'],
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'max_tokens': max_tokens
                },
                timeout=30
            )
            
            print(f"DeepSeek API响应状态码: {response.status_code}")
            print(f"DeepSeek API响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return jsonify({'content': content}), 200
            else:
                return jsonify({'error': f'API调用失败: {response.text}'}), 500
        
        elif model_name == 'qwen':
            response = requests.post(
                model_config['url'],
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                },
                json={
                    'model': model_config['model'],
                    'input': prompt,
                    'parameters': {
                        'max_tokens': max_tokens
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['output']['text']
                return jsonify({'content': content}), 200
            else:
                return jsonify({'error': f'API调用失败: {response.text}'}), 500
        
        elif model_name == 'doubao':
            response = requests.post(
                model_config['url'],
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                },
                json={
                    'model': model_config['model'],
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'max_tokens': max_tokens
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return jsonify({'content': content}), 200
            else:
                return jsonify({'error': f'API调用失败: {response.text}'}), 500
        
        else:
            return jsonify({'error': '不支持的模型'}), 400
            
    except Exception as e:
        print(f"生成失败详细错误: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'生成失败: {str(e)}'}), 500