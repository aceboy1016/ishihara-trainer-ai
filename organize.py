#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from collections import defaultdict
import json

class IshiharaNotesOrganizer:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.raw_notes_file = os.path.join(base_dir, "raw-notes.txt")
        self.current_thoughts_file = os.path.join(base_dir, "current-thoughts.txt")
        self.evolution_log_file = os.path.join(base_dir, "evolution-log.txt")
        
    def parse_raw_notes(self):
        """raw-notes.txtを解析して日付別・テーマ別に整理"""
        if not os.path.exists(self.raw_notes_file):
            print(f"エラー: {self.raw_notes_file} が見つかりません")
            return {}
        
        with open(self.raw_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 日付ごとにメモを分割
        date_pattern = r'(\d{4}-\d{2}-\d{2})'
        entries = re.split(date_pattern, content)
        
        organized_notes = {}
        current_date = None
        
        for entry in entries:
            if re.match(date_pattern, entry):
                current_date = entry
            elif current_date and entry.strip():
                # メモの内容をテーマごとに分類
                notes_lines = [line.strip() for line in entry.strip().split('\n') if line.strip()]
                organized_notes[current_date] = self.categorize_notes(notes_lines)
        
        return organized_notes
    
    def categorize_notes(self, notes_lines):
        """メモをテーマ別に分類"""
        categories = {
            'プロテイン・栄養': [],
            '筋トレ・頻度': [],
            '継続・モチベーション': [],
            '姿勢・体の悩み': [],
            '睡眠': [],
            'お客様との関わり': [],
            '業界への疑問': [],
            'トレーナーとしての気づき': [],
            'その他': []
        }
        
        # キーワードベースでカテゴリ分類
        keyword_map = {
            'プロテイン・栄養': ['プロテイン', '栄養', '食事', 'サプリ'],
            '筋トレ・頻度': ['筋トレ', '頻度', '週', '毎日', 'トレーニング'],
            '継続・モチベーション': ['継続', '楽しく', 'モチベーション', '続け'],
            '姿勢・体の悩み': ['猫背', '反り腰', '腰痛', '姿勢'],
            '睡眠': ['睡眠'],
            'お客様との関わり': ['お客様', '体験', 'セッション'],
            '業界への疑問': ['業界', '広告', '根性論', '画一的'],
            'トレーナーとしての気づき': ['トレーナー', '指導', '完璧', '親近感']
        }
        
        for note in notes_lines:
            categorized = False
            for category, keywords in keyword_map.items():
                if any(keyword in note for keyword in keywords):
                    categories[category].append(note)
                    categorized = True
                    break
            if not categorized:
                categories['その他'].append(note)
        
        # 空のカテゴリを削除
        return {k: v for k, v in categories.items() if v}
    
    def generate_current_thoughts(self, organized_notes):
        """現在の考えを体系的に整理"""
        all_categories = defaultdict(list)
        
        # 全ての日付のメモを統合
        for date, categories in organized_notes.items():
            for category, notes in categories.items():
                for note in notes:
                    all_categories[category].append((date, note))
        
        # 最新の考えを抽出・体系化
        current_thoughts = []
        current_thoughts.append("=== 石原トレーナーの現在の考え・哲学 ===")
        current_thoughts.append(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        current_thoughts.append("")
        
        for category, notes_with_dates in all_categories.items():
            if not notes_with_dates:
                continue
                
            current_thoughts.append(f"【{category}】")
            
            # 最新の考えを優先して整理
            notes_with_dates.sort(key=lambda x: x[0], reverse=True)
            recent_thoughts = []
            
            for date, note in notes_with_dates:
                if not any(self.is_similar_thought(note, existing) for existing in recent_thoughts):
                    recent_thoughts.append(note)
                    if len(recent_thoughts) >= 3:  # 最新の3つの考えまで
                        break
            
            for thought in recent_thoughts:
                current_thoughts.append(f"・{thought}")
            current_thoughts.append("")
        
        return "\n".join(current_thoughts)
    
    def is_similar_thought(self, thought1, thought2):
        """類似する考えかどうかを判定"""
        # 簡単な類似度判定（共通キーワードの比率）
        words1 = set(thought1.split())
        words2 = set(thought2.split())
        if not words1 or not words2:
            return False
        common_ratio = len(words1.intersection(words2)) / len(words1.union(words2))
        return common_ratio > 0.3
    
    def detect_evolution(self, organized_notes):
        """考えの変化を検出"""
        evolution_log = []
        
        # 各カテゴリで時系列での変化を検出
        all_categories = defaultdict(list)
        for date, categories in organized_notes.items():
            for category, notes in categories.items():
                for note in notes:
                    all_categories[category].append((date, note))
        
        for category, notes_with_dates in all_categories.items():
            if len(notes_with_dates) < 2:
                continue
                
            # 日付順にソート
            notes_with_dates.sort(key=lambda x: x[0])
            
            # 変化を検出
            for i in range(1, len(notes_with_dates)):
                prev_date, prev_note = notes_with_dates[i-1]
                curr_date, curr_note = notes_with_dates[i]
                
                # 明らかに異なる考えが出現した場合
                if not self.is_similar_thought(prev_note, curr_note):
                    evolution_entry = {
                        'date': curr_date,
                        'category': category,
                        'previous': prev_note,
                        'current': curr_note,
                        'change_type': '考えの発展'
                    }
                    evolution_log.append(evolution_entry)
        
        return evolution_log
    
    def save_evolution_log(self, evolution_log):
        """変化履歴を保存"""
        if not evolution_log:
            return
            
        log_entries = []
        log_entries.append(f"=== 考えの変化履歴 - {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
        log_entries.append("")
        
        for entry in evolution_log:
            log_entries.append(f"【{entry['date']} - {entry['category']}】")
            log_entries.append(f"変化タイプ: {entry['change_type']}")
            log_entries.append(f"以前の考え: {entry['previous']}")
            log_entries.append(f"現在の考え: {entry['current']}")
            log_entries.append("")
        
        # 既存のログに追記
        if os.path.exists(self.evolution_log_file):
            with open(self.evolution_log_file, 'a', encoding='utf-8') as f:
                f.write("\n" + "\n".join(log_entries))
        else:
            with open(self.evolution_log_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(log_entries))
    
    def organize(self):
        """メイン処理：メモの整理と更新"""
        print("メモを分析中...")
        
        # raw-notes.txtを解析
        organized_notes = self.parse_raw_notes()
        if not organized_notes:
            print("解析できるメモが見つかりませんでした")
            return
        
        # 現在の考えを生成
        current_thoughts = self.generate_current_thoughts(organized_notes)
        
        # current-thoughts.txtを更新
        with open(self.current_thoughts_file, 'w', encoding='utf-8') as f:
            f.write(current_thoughts)
        
        # 考えの変化を検出
        evolution_log = self.detect_evolution(organized_notes)
        
        # 変化履歴を保存
        if evolution_log:
            self.save_evolution_log(evolution_log)
        
        # 結果を報告
        total_notes = sum(len(cats) for cats in organized_notes.values() for cats in cats.values())
        print(f"{len(organized_notes)}日分のメモから{total_notes}個の気づきを発見しました")
        print("current-thoughts.txtを更新しました")
        
        if evolution_log:
            print(f"考えの変化{len(evolution_log)}件をevolution-log.txtに記録しました")
        else:
            print("新しい考えの変化は検出されませんでした")

def main():
    organizer = IshiharaNotesOrganizer()
    organizer.organize()

if __name__ == "__main__":
    main()