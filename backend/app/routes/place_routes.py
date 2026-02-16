from flask import Blueprint, jsonify, request
import json
import os
from ..models.models import Project

place_bp = Blueprint('place', __name__)

# 获取china_regions.json文件的路径
# 使用相对路径，确保在Docker容器中也能正确读取
import os
REGIONS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'china_regions.json')

# 全国省级行政区及简称（带简称）
def get_provinces_with_shortname():
    provinces_with_shortname = []
    # 读取省级数据并添加简称
    with open(REGIONS_FILE_PATH, 'r', encoding='utf-8') as f:
        regions_data = json.load(f)
    
    for province in regions_data.get('省级', []):
        # 提取简称（去掉"省"、"市"、"自治区"、"特别行政区"等后缀）
        short_name = province
        for suffix in ['省', '市', '自治区', '特别行政区']:
            if short_name.endswith(suffix):
                short_name = short_name[:-len(suffix)]
        provinces_with_shortname.append({"name": province, "shortName": short_name})
    
    return provinces_with_shortname

@place_bp.route('/api/places', methods=['GET'])
def get_places():
    """
    获取地名数据，从china_regions.json文件中读取
    """
    try:
        # 读取china_regions.json文件
        with open(REGIONS_FILE_PATH, 'r', encoding='utf-8-sig') as f:
            regions_data = json.load(f)
        
        # 手动构建带简称的省级行政区数据
        provinces_with_shortname = []
        for province in regions_data.get('省级', []):
            # 提取简称（去掉"省"、"市"、"自治区"、"特别行政区"等后缀）
            short_name = province
            for suffix in ['省', '市', '自治区', '特别行政区']:
                if short_name.endswith(suffix):
                    short_name = short_name[:-len(suffix)]
            provinces_with_shortname.append({"name": province, "shortName": short_name})
        
        # 构建返回数据
        result = {
            "provinces": provinces_with_shortname,
            "cities": regions_data.get('市级', []),
            "districts": regions_data.get('区级', [])
        }
        
        return jsonify(result)
    except Exception as e:
        print(f"获取地名数据时发生错误: {str(e)}")
        # 出错时返回空数据
        return jsonify({
            "provinces": [],
            "cities": [],
            "districts": []
        })

@place_bp.route('/api/places/add', methods=['POST'])
def add_place():
    """
    添加新的地名
    """
    try:
        data = request.get_json()
        place = data.get('place')
        level = data.get('level')
        
        if not place or not level:
            return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        
        # 读取china_regions.json文件
        with open(REGIONS_FILE_PATH, 'r', encoding='utf-8-sig') as f:
            regions_data = json.load(f)
        
        # 添加地名到对应级别
        if level == '市级':
            if place not in regions_data.get('市级', []):
                regions_data['市级'].append(place)
        elif level == '区级':
            if place not in regions_data.get('区级', []):
                regions_data['区级'].append(place)
        else:
            return jsonify({'success': False, 'message': '无效的级别'}), 400
        
        # 写回文件
        with open(REGIONS_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(regions_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': '地名添加成功'})
    except Exception as e:
        print(f"添加地名时发生错误: {str(e)}")
        return jsonify({'success': False, 'message': '添加地名失败'}), 500

@place_bp.route('/api/places/delete', methods=['POST'])
def delete_place():
    """
    删除现有的地名
    """
    try:
        data = request.get_json()
        place = data.get('place')
        level = data.get('level')
        
        if not place or not level:
            return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        
        # 读取china_regions.json文件
        with open(REGIONS_FILE_PATH, 'r', encoding='utf-8-sig') as f:
            regions_data = json.load(f)
        
        # 从对应级别删除地名
        if level == '市级':
            if place in regions_data.get('市级', []):
                regions_data['市级'].remove(place)
        elif level == '区级':
            if place in regions_data.get('区级', []):
                regions_data['区级'].remove(place)
        elif level == '省级':
            if place in regions_data.get('省级', []):
                regions_data['省级'].remove(place)
        else:
            return jsonify({'success': False, 'message': '无效的级别'}), 400
        
        # 写回文件
        with open(REGIONS_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(regions_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': '地名删除成功'})
    except Exception as e:
        print(f"删除地名时发生错误: {str(e)}")
        return jsonify({'success': False, 'message': '删除地名失败'}), 500
