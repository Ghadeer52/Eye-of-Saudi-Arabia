#!/usr/bin/env python3
"""
Professional Journalist Script Generator
نظام احترافي لتوليد سكريبتات إعلامية مع تحليل متقدم
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
from datetime import datetime
from collections import Counter
import re

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"


def load_cities_data():
    """تحميل بيانات المدن والمعالم"""
    with open(os.path.join(DATA_DIR, 'cities_landmarks.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class ProfessionalScriptGenerator:
    """مولّد سكريبتات إعلامية احترافية"""
    
    def __init__(self, city: str, landmark: str, duration_seconds: int):
        self.data = load_cities_data()
        self.city = city
        self.landmark = landmark
        self.duration_seconds = duration_seconds
        
        # حساب عدد الكلمات (2.5 كلمة/ثانية للعربية)
        self.target_words = int(duration_seconds * 2.5)
        
        # بيانات المعلم والمدينة
        self.city_data = self.data['cities'][city]
        self.landmark_data = self.city_data['landmarks'][landmark]
        
    def generate(self):
        """توليد سكريبت إعلامي محترف"""
        
        script_sections = []
        
        # 1. العنوان والمقدمة
        title, intro = self._generate_intro()
        script_sections.append(("العنوان", title))
        script_sections.append(("المقدمة", intro))
        
        # 2. الخلفية التاريخية
        if self.duration_seconds >= 90:
            historical = self._generate_historical_context()
            script_sections.append(("الخلفية التاريخية", historical))
        
        # 3. الوصف التفصيلي
        description = self._generate_detailed_description()
        script_sections.append(("الوصف التفصيلي", description))
        
        # 4. الأهمية والتفرد
        if self.duration_seconds >= 60:
            significance = self._generate_significance()
            script_sections.append(("الأهمية والتفرد", significance))
        
        # 5. قصة رئيسية
        if self.duration_seconds >= 120:
            stories = self.landmark_data.get('stories', [])
            if stories:
                story = random.choice(stories)
                story_section = self._format_story(story)
                script_sections.append(("قصة: " + story['title'], story_section))
        
        # 6. المعالم البارزة
        if self.duration_seconds >= 90:
            key_landmarks = self._generate_key_landmarks()
            if key_landmarks:
                script_sections.append(("المعالم البارزة", key_landmarks))
        
        # 7. الأرقام والإحصائيات
        if self.duration_seconds >= 150:
            stats = self._generate_statistics()
            if stats:
                script_sections.append(("أرقام وإحصائيات", stats))
        
        # 8. زوايا صحفية مقترحة
        if self.duration_seconds >= 180:
            angles = self._suggest_journalist_angles()
            if angles:
                script_sections.append(("زوايا صحفية مقترحة", angles))
        
        # 9. معلومات عملية للزيارة
        if self.duration_seconds >= 60:
            visit_info = self._generate_visit_info()
            script_sections.append(("معلومات الزيارة", visit_info))
        
        # 10. الخاتمة
        conclusion = self._generate_conclusion()
        script_sections.append(("الخاتمة", conclusion))
        
        # بناء النص الكامل
        full_script = self._build_full_script(script_sections)
        
        # تحليل السكريبت
        analysis = self._analyze_script(full_script)
        
        return {
            'success': True,
            'script': {
                'title': title,
                'full_text': full_script,
                'sections': [{"title": s[0], "content": s[1]} for s in script_sections],
                'city': self.city_data['name'],
                'city_region': self.city_data.get('region', ''),
                'landmark': self.landmark_data['name'],
                'landmark_type': self.landmark_data['type'],
                'landmark_category': self.landmark_data.get('category', ''),
                'duration_seconds': self.duration_seconds,
                'word_count': len(full_script.split()),
                'char_count': len(full_script),
                'estimated_reading_time': f"{int(len(full_script.split()) / 150)} دقيقة",
                'generated_with': 'Professional Journalist Generator',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                
                # معلومات إضافية للإعلاميين
                'field_questions': self.landmark_data.get('field_questions', []),
                'cultural_notes': self.landmark_data.get('cultural_notes', []),
                'stories': self.landmark_data.get('stories', []),
                'journalist_angles': self.landmark_data.get('journalist_angles', []),
                'statistics': self.landmark_data.get('statistics', {}),
                'references': self.landmark_data.get('references', []),
                'key_landmarks': self.landmark_data.get('key_landmarks', []),
                
                # تحليل النص
                'analysis': analysis
            }
        }
    
    def _generate_intro(self):
        """توليد العنوان والمقدمة"""
        
        # العنوان
        title_templates = [
            f"{self.landmark_data['name']}: {self.landmark_data['category']}",
            f"{self.landmark_data['name']} في {self.city_data['name']} - {self.landmark_data['description']}",
            f"تقرير: {self.landmark_data['name']} - {self.landmark_data['type']}"
        ]
        title = random.choice(title_templates)
        
        # المقدمة
        intro_templates = [
            f"في {self.city_data['name']}، {self.city_data['region']}، يقع {self.landmark_data['name']}، {self.landmark_data['description']}. {self.landmark_data.get('detailed_info', '')}",
            
            f"يُعد {self.landmark_data['name']} أحد أبرز المعالم في {self.city_data['name']}، حيث {self.landmark_data['description']}. {self.landmark_data.get('detailed_info', '')}",
            
            f"{self.landmark_data['name']} - {self.landmark_data['category']} - معلم استثنائي في {self.city_data['name']} {self.landmark_data['description']}. {self.landmark_data.get('detailed_info', '')}"
        ]
        
        intro = random.choice(intro_templates)
        
        # إضافة معلومات اليونسكو إذا كانت موجودة
        info = self.landmark_data.get('info', {})
        if info.get('unesco'):
            year = info.get('year_inscribed', 'غير محدد')
            unesco_criteria = info.get('unesco_criteria', '')
            unesco_name = info.get('inscription_name', self.landmark_data['name'])
            intro += f" الموقع مُدرج في قائمة التراث العالمي لليونسكو منذ عام {year}م تحت اسم '{unesco_name}'"
            if unesco_criteria:
                intro += f" وفقاً لـ{unesco_criteria}"
            intro += "."
        
        return title, intro
    
    def _generate_historical_context(self):
        """السياق التاريخي"""
        
        historical = self.landmark_data.get('historical_significance', '')
        
        if not historical:
            # توليد سياق عام
            age = self.landmark_data.get('info', {}).get('age', '')
            if age:
                historical = f"يعود تاريخ {self.landmark_data['name']} إلى {age}، مما يجعله شاهداً على حقب تاريخية متعددة."
        
        return historical
    
    def _generate_detailed_description(self):
        """الوصف التفصيلي"""
        
        parts = []
        
        # المعلومات المعمارية أو الطبيعية
        arch_features = self.landmark_data.get('architectural_features', {})
        if arch_features:
            parts.append("من الناحية المعمارية:")
            for feature, desc in list(arch_features.items())[:3]:
                parts.append(f"- {feature.replace('_', ' ').title()}: {desc}")
        
        # الأهمية الأثرية
        arch_importance = self.landmark_data.get('archaeological_importance', '')
        if arch_importance:
            parts.append(arch_importance)
        
        # التطور التاريخي
        development = self.landmark_data.get('historical_development', '')
        if development:
            parts.append(development)
        
        if not parts:
            parts.append(self.landmark_data['detailed_info'])
        
        return "\n\n".join(parts)
    
    def _generate_significance(self):
        """الأهمية والتفرد"""
        
        significance_parts = []
        
        # الأهمية التاريخية
        hist_sig = self.landmark_data.get('historical_significance', '')
        if hist_sig:
            significance_parts.append(f"تاريخياً: {hist_sig}")
        
        # الأهمية الثقافية
        if self.landmark_data.get('info', {}).get('unesco'):
            significance_parts.append(f"ثقافياً: يمثل {self.landmark_data['name']} قيمة عالمية استثنائية، كما أقرته منظمة اليونسكو.")
        
        # الأهمية الاقتصادية
        stats = self.landmark_data.get('statistics', {})
        if stats.get('annual_visitors_2023'):
            significance_parts.append(f"اقتصادياً: استقبل الموقع {stats['annual_visitors_2023']} زائر في 2023، مما يجعله محركاً اقتصادياً مهماً.")
        
        return "\n\n".join(significance_parts) if significance_parts else ""
    
    def _format_story(self, story):
        """تنسيق القصة"""
        
        formatted = story['content']
        
        # إضافة معلومات إضافية
        if story.get('year'):
            formatted = f"[{story['year']}]\n\n{formatted}"
        
        if story.get('sources'):
            sources = ', '.join(story['sources'][:3])
            formatted += f"\n\nالمصادر: {sources}"
        
        if story.get('type'):
            formatted += f"\n\nالنوع: {story['type']}"
        
        return formatted
    
    def _generate_key_landmarks(self):
        """المعالم البارزة"""
        
        key_landmarks = self.landmark_data.get('key_landmarks', [])
        
        if not key_landmarks:
            return ""
        
        # اختيار عدد بناءً على المدة
        num = min(len(key_landmarks), max(2, int(self.duration_seconds / 60)))
        selected = random.sample(key_landmarks, num)
        
        parts = []
        for lm in selected:
            desc = f"• {lm['name']}"
            if lm.get('year'):
                desc += f" ({lm['year']})"
            desc += f": {lm['description']}"
            
            if lm.get('significance'):
                desc += f" الأهمية: {lm['significance']}"
            
            parts.append(desc)
        
        return "\n\n".join(parts)
    
    def _generate_statistics(self):
        """الأرقام والإحصائيات"""
        
        stats = self.landmark_data.get('statistics', {})
        
        if not stats:
            return ""
        
        parts = ["الأرقام تتحدث:"]
        
        for key, value in stats.items():
            # تنسيق المفتاح
            key_formatted = key.replace('_', ' ').title()
            parts.append(f"• {key_formatted}: {value}")
        
        return "\n".join(parts)
    
    def _suggest_journalist_angles(self):
        """زوايا صحفية مقترحة"""
        
        angles = self.landmark_data.get('journalist_angles', [])
        
        if not angles:
            return ""
        
        # اختيار 3-5 زوايا عشوائياً
        num = min(len(angles), 5)
        selected = random.sample(angles, num)
        
        parts = ["زوايا صحفية مقترحة للتغطية:"]
        for i, angle in enumerate(selected, 1):
            parts.append(f"{i}. {angle}")
        
        return "\n".join(parts)
    
    def _generate_visit_info(self):
        """معلومات الزيارة"""
        
        info = self.landmark_data.get('info', {})
        
        parts = ["معلومات عملية للزيارة:"]
        
        if info.get('best_time'):
            parts.append(f"• أفضل وقت: {info['best_time']}")
        
        if info.get('duration'):
            parts.append(f"• المدة المقترحة: {info['duration']}")
        
        if info.get('entry_fee'):
            parts.append(f"• رسوم الدخول: {info['entry_fee']}")
        
        if info.get('guided_tours'):
            parts.append(f"• الجولات المصحوبة: {info['guided_tours']}")
        
        return "\n".join(parts)
    
    def _generate_conclusion(self):
        """الخاتمة"""
        
        conclusions = [
            f"يظل {self.landmark_data['name']} شاهداً على عظمة التاريخ والحضارة، ومعلماً يستحق الزيارة والدراسة المعمقة.",
            
            f"بين الماضي والحاضر، يقف {self.landmark_data['name']} كجسر يربط الأجيال، ويروي قصة {self.city_data['name']} العريقة.",
            
            f"يواصل {self.landmark_data['name']} جذب الباحثين والزوار من مختلف أنحاء العالم، مؤكداً مكانته كأحد أهم المعالم في المملكة.",
            
            f"في عصر التحول والتطوير، يحافظ {self.landmark_data['name']} على هويته التاريخية، مقدماً للعالم نموذجاً فريداً للحفاظ على التراث."
        ]
        
        return random.choice(conclusions)
    
    def _build_full_script(self, sections):
        """بناء النص الكامل"""
        
        # النص الكامل بدون عناوين الأقسام
        parts = []
        for title, content in sections:
            if title != "العنوان":  # تخطي العنوان في النص
                parts.append(content)
        
        return "\n\n".join(parts)
    
    def _analyze_script(self, script):
        """تحليل السكريبت"""
        
        words = script.split()
        sentences = script.split('.')
        
        # عدد الكلمات والجمل
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # متوسط طول الجملة
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # الكلمات الأكثر تكراراً
        word_freq = Counter([w.strip('.,!?؛:') for w in words if len(w) > 3])
        most_common = word_freq.most_common(10)
        
        # نسبة القراءة
        readability = "سهل" if avg_sentence_length < 15 else "متوسط" if avg_sentence_length < 25 else "متقدم"
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'readability': readability,
            'most_common_words': most_common[:5],
            'paragraph_count': script.count('\n\n') + 1
        }


class AdvancedScriptAnalyzer:
    """محلل سكريبتات متقدم مع توصيات احترافية"""
    
    def __init__(self, script_text: str):
        self.script_text = script_text
        self.words = script_text.split()
        self.sentences = [s.strip() for s in script_text.split('.') if s.strip()]
        
    def analyze(self):
        """تحليل شامل مع توصيات"""
        
        # التحليل الأساسي
        basic_analysis = self._basic_analysis()
        
        # تحليل الأسلوب
        style_analysis = self._style_analysis()
        
        # تحليل المحتوى
        content_analysis = self._content_analysis()
        
        # التوصيات
        recommendations = self._generate_recommendations(basic_analysis, style_analysis, content_analysis)
        
        # التقييم الشامل
        overall_score = self._calculate_overall_score(basic_analysis, style_analysis, content_analysis)
        
        return {
            'success': True,
            'analysis': {
                'basic': basic_analysis,
                'style': style_analysis,
                'content': content_analysis,
                'recommendations': recommendations,
                'overall_score': overall_score,
                'analyzed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    
    def _basic_analysis(self):
        """التحليل الأساسي"""
        
        word_count = len(self.words)
        sentence_count = len(self.sentences)
        char_count = len(self.script_text)
        paragraph_count = self.script_text.count('\n\n') + 1
        
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        avg_word_length = sum(len(w) for w in self.words) / word_count if word_count > 0 else 0
        
        # وقت القراءة المقدر (150 كلمة/دقيقة)
        reading_time = word_count / 150
        
        # وقت البث المقدر (2.5 كلمة/ثانية)
        broadcast_time = word_count / 2.5
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'char_count': char_count,
            'paragraph_count': paragraph_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 1),
            'reading_time_minutes': round(reading_time, 1),
            'broadcast_time_seconds': int(broadcast_time)
        }
    
    def _style_analysis(self):
        """تحليل الأسلوب"""
        
        # الكشف عن الأسلوب الإعلامي
        journalist_indicators = [
            'يقع', 'تقع', 'يُعد', 'تُعد', 'يشير', 'تشير', 'وفقاً', 
            'حيث', 'إذ', 'بينما', 'من جهة', 'من ناحية', 'تاريخياً', 
            'حالياً', 'مستقبلاً', 'المصادر', 'التقارير', 'الدراسات'
        ]
        
        journalist_score = sum(1 for word in journalist_indicators if word in self.script_text)
        
        # الموضوعية (غياب الضمائر الشخصية)
        personal_pronouns = ['أنا', 'نحن', 'أشعر', 'أرى', 'أعتقد']
        objectivity_score = 100 - (sum(1 for word in personal_pronouns if word in self.script_text) * 10)
        objectivity_score = max(0, min(100, objectivity_score))
        
        # الدقة (وجود أرقام وتواريخ)
        numbers = len(re.findall(r'\d+', self.script_text))
        has_dates = len(re.findall(r'\d{4}', self.script_text)) > 0
        
        # الهيكلية (الفقرات المنظمة)
        has_structure = self.script_text.count('\n\n') >= 2
        
        return {
            'style_type': 'إعلامي محترف' if journalist_score >= 5 else 'عام',
            'journalist_score': journalist_score,
            'objectivity': f"{objectivity_score}%",
            'uses_data': numbers > 0,
            'numbers_count': numbers,
            'has_dates': has_dates,
            'well_structured': has_structure,
            'tone': self._detect_tone()
        }
    
    def _detect_tone(self):
        """الكشف عن النبرة"""
        
        formal_words = ['يُعد', 'تُعتبر', 'يشير', 'وفقاً', 'حيث', 'إذ']
        informal_words = ['رائع', 'جميل', 'مذهل', 'خيالي']
        
        formal_count = sum(1 for word in formal_words if word in self.script_text)
        informal_count = sum(1 for word in informal_words if word in self.script_text)
        
        if formal_count > informal_count * 2:
            return "رسمي"
        elif informal_count > formal_count:
            return "غير رسمي"
        else:
            return "متوازن"
    
    def _content_analysis(self):
        """تحليل المحتوى"""
        
        # الكلمات الأكثر تكراراً
        word_freq = Counter([w.strip('.,!?؛:') for w in self.words if len(w) > 3])
        most_common = word_freq.most_common(10)
        
        # الموضوعات المحتملة
        topics = []
        topic_keywords = {
            'تاريخ': ['تاريخ', 'قديم', 'عصر', 'حقبة', 'قرن'],
            'ثقافة': ['ثقافة', 'تراث', 'عمارة', 'فن'],
            'سياحة': ['سياحة', 'زوار', 'زيارة', 'جولة'],
            'اقتصاد': ['اقتصاد', 'استثمار', 'تنمية', 'وظائف']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in self.script_text for kw in keywords):
                topics.append(topic)
        
        # وجود اقتباسات أو مصادر
        has_quotes = '"' in self.script_text or "'" in self.script_text
        mentions_sources = any(word in self.script_text for word in ['المصادر', 'المرجع', 'الدراسة', 'التقرير'])
        
        return {
            'most_common_words': [{'word': word, 'count': count} for word, count in most_common[:5]],
            'topics_covered': topics,
            'has_quotes': has_quotes,
            'mentions_sources': mentions_sources,
            'diversity_score': len(set(self.words)) / len(self.words) if self.words else 0
        }
    
    def _generate_recommendations(self, basic, style, content):
        """توليد التوصيات"""
        
        recommendations = []
        
        # توصيات بناءً على الطول
        if basic['word_count'] < 100:
            recommendations.append({
                'type': 'الطول',
                'priority': 'عالية',
                'issue': 'السكريبت قصير جداً',
                'suggestion': 'أضف المزيد من التفاصيل والمعلومات الخلفية. السكريبت الإعلامي الجيد يتراوح بين 200-500 كلمة.'
            })
        elif basic['word_count'] > 600:
            recommendations.append({
                'type': 'الطول',
                'priority': 'متوسطة',
                'issue': 'السكريبت طويل قد يكون مملاً',
                'suggestion': 'حاول الاختصار والتركيز على النقاط الرئيسية. قسّم المحتوى إلى تقريرين منفصلين إذا لزم الأمر.'
            })
        
        # توصيات بناءً على الأسلوب
        if style['journalist_score'] < 3:
            recommendations.append({
                'type': 'الأسلوب',
                'priority': 'عالية',
                'issue': 'الأسلوب غير إعلامي بما يكفي',
                'suggestion': 'استخدم عبارات إعلامية احترافية مثل: "وفقاً للمصادر"، "تشير التقارير"، "من الجدير بالذكر". تجنب الضمائر الشخصية.'
            })
        
        if int(style['objectivity'].rstrip('%')) < 80:
            recommendations.append({
                'type': 'الموضوعية',
                'priority': 'عالية',
                'issue': 'السكريبت يحتوي على آراء شخصية',
                'suggestion': 'حافظ على الحياد الصحفي. استبدل الآراء الشخصية بحقائق وبيانات موثقة.'
            })
        
        # توصيات بناءً على المحتوى
        if not style['uses_data']:
            recommendations.append({
                'type': 'البيانات',
                'priority': 'متوسطة',
                'issue': 'عدم وجود أرقام أو إحصائيات',
                'suggestion': 'أضف أرقاماً وإحصائيات لدعم المعلومات. مثل: عدد الزوار، التكلفة، المساحة، التواريخ المحددة.'
            })
        
        if not content['mentions_sources']:
            recommendations.append({
                'type': 'المصادر',
                'priority': 'عالية',
                'issue': 'عدم ذكر المصادر',
                'suggestion': 'اذكر مصادر المعلومات لزيادة المصداقية. مثل: "وفقاً لتقرير اليونسكو"، "حسب بيانات الهيئة".'
            })
        
        if basic['paragraph_count'] < 3:
            recommendations.append({
                'type': 'الهيكلة',
                'priority': 'متوسطة',
                'issue': 'السكريبت غير منظم في فقرات',
                'suggestion': 'قسّم السكريبت إلى فقرات واضحة: مقدمة، جسم (2-3 فقرات)، خاتمة.'
            })
        
        if basic['avg_sentence_length'] > 25:
            recommendations.append({
                'type': 'القراءة',
                'priority': 'متوسطة',
                'issue': 'الجمل طويلة جداً',
                'suggestion': 'اختصر الجمل لتكون أسهل في القراءة والفهم. الجملة المثالية: 15-20 كلمة.'
            })
        
        # إذا لم تكن هناك مشاكل
        if not recommendations:
            recommendations.append({
                'type': 'عام',
                'priority': 'معلومة',
                'issue': 'لا توجد مشاكل كبيرة',
                'suggestion': 'السكريبت احترافي وجيد البناء. استمر على هذا المستوى!'
            })
        
        return recommendations
    
    def _calculate_overall_score(self, basic, style, content):
        """حساب التقييم الشامل"""
        
        score = 0
        max_score = 100
        
        # الطول (20 نقطة)
        if 200 <= basic['word_count'] <= 500:
            score += 20
        elif 150 <= basic['word_count'] < 200 or 500 < basic['word_count'] <= 600:
            score += 15
        else:
            score += 10
        
        # الأسلوب الإعلامي (25 نقطة)
        score += min(25, style['journalist_score'] * 3)
        
        # الموضوعية (15 نقطة)
        objectivity = int(style['objectivity'].rstrip('%'))
        score += objectivity * 0.15
        
        # استخدام البيانات (15 نقطة)
        if style['uses_data']:
            score += 10
        if style['has_dates']:
            score += 5
        
        # ذكر المصادر (10 نقطة)
        if content['mentions_sources']:
            score += 10
        
        # الهيكلية (10 نقطة)
        if basic['paragraph_count'] >= 3:
            score += 5
        if style['well_structured']:
            score += 5
        
        # التنوع اللغوي (5 نقاط)
        diversity = content['diversity_score']
        score += diversity * 5
        
        score = min(max_score, round(score, 1))
        
        # التقييم النصي
        if score >= 90:
            rating = "ممتاز"
        elif score >= 75:
            rating = "جيد جداً"
        elif score >= 60:
            rating = "جيد"
        elif score >= 50:
            rating = "مقبول"
        else:
            rating = "يحتاج تحسين"
        
        return {
            'score': score,
            'rating': rating,
            'max_score': max_score
        }


# ============= API Endpoints =============

@app.route('/')
def home():
    return jsonify({
        'service': 'Professional Journalist Script Generator',
        'version': '4.0',
        'mode': 'Journalist Only',
        'features': [
            'سكريبتات إعلامية احترافية طويلة',
            'بيانات موسّعة وحقيقية',
            'تحليل متقدم مع توصيات',
            'قصص تاريخية مفصلة',
            'زوايا صحفية مقترحة'
        ]
    })


@app.route('/api/cities', methods=['GET'])
def get_cities():
    data = load_cities_data()
    
    cities_list = []
    for city_id, city_info in data['cities'].items():
        cities_list.append({
            'id': city_id,
            'name': city_info['name'],
            'name_en': city_info['name_en'],
            'icon': city_info['icon'],
            'description': city_info['description'],
            'region': city_info.get('region', ''),
            'population': city_info.get('population', ''),
            'landmarks_count': len(city_info['landmarks'])
        })
    
    return jsonify({'success': True, 'cities': cities_list})


@app.route('/api/cities/<city_id>/landmarks', methods=['GET'])
def get_landmarks(city_id):
    data = load_cities_data()
    
    if city_id not in data['cities']:
        return jsonify({'success': False, 'error': 'City not found'}), 404
    
    city = data['cities'][city_id]
    landmarks_list = []
    
    for landmark_id, landmark_info in city['landmarks'].items():
        landmarks_list.append({
            'id': landmark_id,
            'name': landmark_info['name'],
            'icon': landmark_info['icon'],
            'type': landmark_info['type'],
            'category': landmark_info.get('category', ''),
            'description': landmark_info['description'],
            'has_stories': len(landmark_info.get('stories', [])) > 0,
            'stories_count': len(landmark_info.get('stories', [])),
            'unesco': landmark_info.get('info', {}).get('unesco', False)
        })
    
    return jsonify({
        'success': True,
        'city': {
            'id': city_id,
            'name': city['name'],
            'icon': city['icon'],
            'region': city.get('region', '')
        },
        'landmarks': landmarks_list
    })


@app.route('/api/generate', methods=['POST'])
def generate_script():
    data = request.get_json()
    
    required_fields = ['city', 'landmark', 'duration']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    try:
        generator = ProfessionalScriptGenerator(
            city=data['city'],
            landmark=data['landmark'],
            duration_seconds=data['duration']
        )
        
        result = generator.generate()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_script():
    data = request.get_json()
    
    if 'script' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing script text'
        }), 400
    
    try:
        analyzer = AdvancedScriptAnalyzer(data['script'])
        result = analyzer.analyze()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 80)
    print("🎙️  Professional Journalist Script Generator")
    print("=" * 80)
    print("📰 Mode: Journalist Only (Professional)")
    print("📚 Features: Long scripts + Advanced analysis + Recommendations")
    print("")
    
    data = load_cities_data()
    total_landmarks = sum(len(city['landmarks']) for city in data['cities'].values())
    total_stories = sum(
        len(landmark.get('stories', []))
        for city in data['cities'].values()
        for landmark in city['landmarks'].values()
    )
    
    print(f"📊 Cities: {len(data['cities'])}")
    print(f"📊 Landmarks: {total_landmarks}")
    print(f"📖 Stories: {total_stories}")
    print("\n" + "=" * 80)
    print("🌐 Server: http://localhost:5000/")
    print("=" * 80 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
