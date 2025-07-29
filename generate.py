#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from datetime import datetime
import random

class IshiharaArticleGenerator:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.style_guide_file = os.path.join(base_dir, "style-guide.txt")
        self.current_thoughts_file = os.path.join(base_dir, "current-thoughts.txt")
        self.output_dir = os.path.join(base_dir, "output")
        
        # 石原トレーナーの表現パターン
        self.expressions = {
            'opening': [
                "みなさんこんにちは。トレーナーの石原です。",
                "みなさん、こんにちは！トレーナーの石原です。"
            ],
            'problem_introduction': [
                "よく体験にいらっしゃる方から寄せられる{topic}で多い声が、",
                "最近、お客様から{topic}についてよく相談されます。",
                "セッションの中で{topic}についてお話しすることが多いのですが、"
            ],
            'empathy_check': [
                "聞き馴染みがあるのではないでしょうか？？",
                "心当たりがある方も多いのではないでしょうか？？",
                "ご経験がある方もいらっしゃるのではないでしょうか？？"
            ],
            'common_advice': [
                "よくあるアドバイスとしては、",
                "一般的には、",
                "多くの場合、"
            ],
            'balance_evaluation': [
                "決して間違いではありませんし、これで解決するケースも少なくありません。",
                "確かにこれも大切ですし、効果的な方法の一つです。",
                "もちろん、これも有効な方法だと思います。"
            ],
            'transition': [
                "ただ、人の体はそう単純ではなく",
                "しかし、実際にはもう少し複雑で",
                "ですが、根本的な解決を考えると"
            ],
            'question_transition': [
                "じゃあ何をすればいいの？",
                "では、具体的にはどうすればいいのでしょうか？",
                "そこで今回は、"
            ],
            'experience_invitation': [
                "やってみていかがでしょうか。",
                "ぜひ試してみてください。",
                "一度実践してみていただければと思います。"
            ],
            'encouragement': [
                "（いつもお仕事お疲れ様です。）",
                "（お忙しい中、お疲れ様です。）",
                "（日々お疲れ様です。）"
            ],
            'closing': [
                "今回は、ここまで。",
                "今日はここまでです。",
                "本日はここまでとさせていただきます。"
            ],
            'continuation': [
                "反応があれば、この続きを書いていきたいと思います。",
                "ご質問やご感想があれば、続きを書かせていただきますね。",
                "皆さんの反応次第で、詳しい内容もお伝えしていきます。"
            ]
        }
    
    def load_style_guide(self):
        """スタイルガイドを読み込み"""
        if not os.path.exists(self.style_guide_file):
            print(f"警告: {self.style_guide_file} が見つかりません")
            return ""
        
        with open(self.style_guide_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_current_thoughts(self):
        """現在の考えを読み込み"""
        if not os.path.exists(self.current_thoughts_file):
            print(f"警告: {self.current_thoughts_file} が見つかりません")
            return ""
        
        with open(self.current_thoughts_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_relevant_thoughts(self, topic, current_thoughts):
        """テーマに関連する考えを抽出"""
        if not current_thoughts:
            return []
        
        # テーマに関連するキーワードマッピング
        topic_keywords = {
            'プロテイン': ['プロテイン', '栄養', '食事', 'サプリ'],
            '筋トレ': ['筋トレ', 'トレーニング', '頻度', '継続'],
            '姿勢': ['猫背', '反り腰', '姿勢', '腰痛'],
            '継続': ['継続', 'モチベーション', '楽しく'],
            '睡眠': ['睡眠'],
            '食事': ['食事', '栄養', 'プロテイン']
        }
        
        # テーマに最も近いキーワードセットを見つける
        relevant_keywords = []
        for key, keywords in topic_keywords.items():
            if key in topic or any(keyword in topic for keyword in keywords):
                relevant_keywords.extend(keywords)
        
        # 関連する考えを抽出
        relevant_thoughts = []
        for line in current_thoughts.split('\n'):
            if line.strip().startswith('・') and any(keyword in line for keyword in relevant_keywords):
                relevant_thoughts.append(line.strip()[1:].strip())  # '・'を除去
        
        return relevant_thoughts
    
    def generate_note_article(self, topic, relevant_thoughts):
        """note用記事生成（3000-5000文字）"""
        article = []
        
        # タイトル
        article.append(f"# {topic}")
        article.append("")
        
        # 導入
        article.append(random.choice(self.expressions['opening']))
        article.append(f"今回は、{topic}について詳しくお伝えいたします。")
        article.append("")
        
        # 問題提起
        problem_intro = random.choice(self.expressions['problem_introduction']).format(topic=f"{topic}に関する悩み")
        article.append(problem_intro)
        
        # よくある悩み例（テーマに応じて）
        if 'プロテイン' in topic:
            article.append('「プロテインって本当に必要ですか？」')
            article.append('「どのプロテインを選べばいいかわからない」')
            article.append('「プロテインを飲んでるけど効果を感じない」')
        elif '筋トレ' in topic:
            article.append('「どのくらいの頻度でやればいいですか？」')
            article.append('「毎日やらないと意味がないですか？」')
            article.append('「忙しくて続けられません」')
        elif '姿勢' in topic:
            article.append('「猫背が気になって仕方ない」')
            article.append('「デスクワークで肩こりがひどい」')
            article.append('「反り腰で腰が痛い」')
        
        article.append("")
        article.append(random.choice(self.expressions['empathy_check']))
        article.append("")
        
        # 一般的なアドバイスとバランス評価
        article.append(random.choice(self.expressions['common_advice']))
        if 'プロテイン' in topic:
            article.append('「とりあえず有名なプロテインを買って飲んでください」')
        elif '筋トレ' in topic:
            article.append('「毎日少しずつでも続けましょう」')
        elif '姿勢' in topic:
            article.append('「背筋を伸ばして正しい姿勢を心がけましょう」')
        
        article.append("")
        article.append(random.choice(self.expressions['balance_evaluation']))
        article.append(random.choice(self.expressions['transition']) + "...")
        article.append("")
        
        # 石原トレーナーの考え（現在の考えから抽出）
        article.append("## 私が考える、より効果的なアプローチ")
        article.append("")
        
        if relevant_thoughts:
            for i, thought in enumerate(relevant_thoughts[:3], 1):  # 最大3つ
                article.append(f"### {i}. {self.extract_title_from_thought(thought)}")
                article.append("")
                article.append(self.expand_thought_for_note(thought))
                article.append("")
        else:
            # デフォルトのアドバイス
            article.append("### 1. 個人差を理解する")
            article.append("")
            article.append("まず大切なのは、一人ひとりの体は違うということです。")
            article.append("同じ方法でも効果の出方は人それぞれ。")
            article.append("ここから推察するに、画一的なアドバイスではなく、")
            article.append("あなたに合った方法を見つけることが重要だと思っています。")
            article.append("")
        
        # 実践的なアドバイス
        article.append("## 具体的に何から始めるか")
        article.append("")
        article.append("理論も大切ですが、やっぱり実践が一番です。")
        article.append("")
        
        if 'プロテイン' in topic:
            article.append("まず、現在の食事でたんぱく質がどのくらい摂れているかを確認してみてください。")
            article.append("プロテインパウダーありきではなく、食事からの摂取も検討してみましょう。")
            article.append("そして、継続しやすい味や形状を重視して選ぶことが大切です。")
        elif '筋トレ' in topic:
            article.append("まず、週1回からでも始めてみてください。完璧を求める必要はありません。")
            article.append("楽しめる種目を見つけることから始めましょう。")
            article.append("結果より継続することを優先してみてください。")
        elif '姿勢' in topic:
            article.append("まず、日常の座り方・立ち方を見直してみてください。")
            article.append("エクササイズだけでなく、デスク環境なども整えてみましょう。")
            article.append("完璧な姿勢より、まずは「気づく」習慣をつけることが大切です。")
        
        article.append("")
        article.append(random.choice(self.expressions['experience_invitation']))
        article.append(random.choice(self.expressions['encouragement']))
        article.append("")
        
        # 締め
        article.append("## おわりに")
        article.append("")
        article.append(f"{topic}について、私なりの考えをお伝えいたしました。")
        article.append("")
        article.append("大切なのは、正しい方法よりもあなたが続けられる方法。")
        article.append("完璧を目指すより、継続を目指す。")
        article.append("")
        article.append("そんな気持ちで、一歩ずつ取り組んでいただければと思います。")
        article.append("")
        article.append(random.choice(self.expressions['closing']))
        article.append(random.choice(self.expressions['continuation']))
        article.append("")
        article.append("---")
        article.append("")
        article.append("**パーソナルトレーニングにご興味のある方は、**")
        article.append("**体験セッションからお気軽にどうぞ。**")
        
        return "\n".join(article)
    
    def generate_ameblo_article(self, topic, relevant_thoughts):
        """ameblo用記事生成（1000-2000文字）"""
        article = []
        
        # タイトル
        article.append(f"# {topic}")
        article.append("")
        
        # 導入（よりカジュアル）
        article.append(random.choice(self.expressions['opening']))
        article.append(f"今回は、{topic}についてご紹介します✨")
        article.append("")
        
        # 問題提起（簡潔に）
        problem_intro = random.choice(self.expressions['problem_introduction']).format(topic=f"{topic}の悩み")
        article.append(problem_intro)
        
        if 'プロテイン' in topic:
            article.append('「プロテインって必要？」')
            article.append('「どれを選べばいいの？」')
        elif '筋トレ' in topic:
            article.append('「どのくらいやればいいの？」')
            article.append('「続かない💦」')
        elif '姿勢' in topic:
            article.append('「猫背が気になる」')
            article.append('「肩こりがひどい」')
        
        article.append("")
        article.append(random.choice(self.expressions['empathy_check']))
        article.append("")
        
        # 体験談・関西弁要素を入れる
        article.append("## 私の体験談")
        article.append("")
        if 'プロテイン' in topic:
            article.append("実は私も昔、プロテイン選びで迷いまくってました😅")
            article.append("「高いやつの方がいいんかな？」って思って")
            article.append("結局続かへんかったという...")
        elif '筋トレ' in topic:
            article.append("お客様に「週何回やればいいですか？」って")
            article.append("よく聞かれるんですが、")
            article.append("正直、毎日やらなくても全然オッケーやと思ってます！")
        elif '姿勢' in topic:
            article.append("デスクワークのお客様から")
            article.append("「猫背が気になって...」って相談されること多いです")
            article.append("でも「背筋を伸ばして」だけじゃ根本解決にならへんのよね💦")
        
        article.append("")
        
        # 石原トレーナーのアドバイス（1-2個に絞る）
        article.append("## 私が思うポイント")
        article.append("")
        
        if relevant_thoughts:
            thought = relevant_thoughts[0]  # 最初の1つだけ使用
            article.append(f"**{self.extract_title_from_thought(thought)}**")
            article.append("")
            article.append(self.expand_thought_for_ameblo(thought))
        else:
            article.append("**完璧を求めずに継続を優先**")
            article.append("")
            article.append("一番大事なのは続けること！")
            article.append("完璧にやろうとして挫折するより、")
            article.append("6割でも続ける方が絶対にいい結果が出ます✨")
        
        article.append("")
        
        # 具体的なアクション（簡潔に）
        article.append("## 今日からできること")
        article.append("")
        
        if 'プロテイン' in topic:
            article.append("まずは今の食事を見直してみてください。")
            article.append("足りない分だけプロテインで補うという考え方で十分です。")
            article.append("続けやすい味を選ぶことも大切ですね。")
        elif '筋トレ' in topic:
            article.append("週1回からスタートしてみてください。")
            article.append("楽しめる種目を見つけることから始めましょう。")
            article.append("習慣になったら少しずつ増やしていけばいいんです。")
        elif '姿勢' in topic:
            article.append("座り方をちょっと意識してみてください。")
            article.append("1時間に1回立ち上がる習慣をつけてみましょう。")
            article.append("簡単なストレッチを取り入れてみるのもおすすめです。")
        
        article.append("")
        article.append(random.choice(self.expressions['experience_invitation']))
        article.append("")
        
        # 親しみやすい締め
        article.append("一緒に頑張りましょうね〜😊")
        article.append(random.choice(self.expressions['encouragement']))
        article.append("")
        article.append(random.choice(self.expressions['closing']))
        article.append("質問があればお気軽にコメントください💪")
        article.append("")
        article.append("---")
        article.append("")
        article.append("パーソナルトレーニング体験受付中✨")
        article.append("お気軽にDMくださいね〜")
        
        return "\n".join(article)
    
    def generate_kensuu_style_blog(self, topic, relevant_thoughts):
        """けんすうスタイル×石原トレーナーのブログ記事生成"""
        article = []
        
        # タイトル
        article.append(f"# {topic}")
        article.append("")
        
        # けんすう式導入
        article.append("こんにちは！トレーナーの石原です。")
        article.append("")
        article.append(f"今日は「{topic}」について書きたいと思います。")
        
        # 問題提起・共感
        if 'プロテイン' in topic:
            problem = "「プロテインって本当に必要ですか？」「どれを選べばいいかわからない」"
            common_advice = "「とりあえず有名なプロテインを買って飲んでください」"
        elif '筋トレ' in topic or 'トレーニング' in topic:
            problem = "「どのくらいの頻度でやればいいですか？」「毎日やらないと意味がないですか？」"
            common_advice = "「毎日少しずつでも続けましょう」"
        elif '姿勢' in topic:
            problem = "「猫背が気になって仕方ない」「デスクワークで肩こりがひどい」"
            common_advice = "「背筋を伸ばして正しい姿勢を心がけましょう」"
        else:
            problem = f"「{topic}について悩んでいます」"
            common_advice = "「頑張って継続しましょう」"
        
        article.append(f"最近、お客様から{problem}という相談をよく受けるんですよね。")
        article.append("")
        article.append("みなさんもきっと一度は言われたことがあると思うんです。")
        
        # 一般的なアドバイスの提示
        article.append("")
        article.append("## よくあるアドバイスの落とし穴")
        article.append("")
        article.append(f"{topic}でよく言われるのが{common_advice}というアドバイスです。")
        article.append("")
        article.append("これ、間違いではないんですが、ちょっと問題があるんですよね。")
        article.append("")
        
        # 問題点の指摘（けんすう式）
        if '姿勢' in topic:
            article.append("まず、意識し続けるのがめちゃくちゃ疲れます。")
            article.append("朝は頑張って背筋を伸ばしていても、昼過ぎには「あ、また猫背になってる...」ってなりがちです。")
            article.append("")
            article.append("しかも「正しい姿勢」って、実は人によって違うんです。")
        elif 'プロテイン' in topic:
            article.append("まず、「有名だから良い」とは限らないということです。")
            article.append("味や値段、続けやすさは人それぞれ違いますからね。")
            article.append("")
            article.append("しかも、そもそも本当にプロテインが必要かどうかも、その人の食事によって変わります。")
        elif '筋トレ' in topic:
            article.append("まず、「毎日」というプレッシャーがしんどいです。")
            article.append("できない日があると「今日もサボってしまった...」という罪悪感に襲われます。")
            article.append("")
            article.append("しかも、毎日やることが必ずしも効果的とは限らないんです。")
        
        article.append("")
        article.append("骨格も筋肉のつき方も、日常の動作パターンも人それぞれ。")
        article.append("なのに画一的なアドバイスをもらっても、根本的な解決にはならないことが多いんです。")
        
        # 視点の転換（けんすう式）
        article.append("")
        article.append(f"## {topic.replace('の', '')}が難しい本当の理由")
        article.append("")
        article.append("ここで少し視点を変えてみましょう。")
        article.append("")
        
        if '姿勢' in topic:
            article.append("そもそも、なぜ姿勢が悪くなるのか。")
            article.append("多くの場合、それは「楽だから」なんです。")
            article.append("猫背の方が、その人の体にとって楽な状態になってしまっているんですね。")
            article.append("")
            article.append("例えば、デスクワークで前かがみになる時間が長いと、胸の筋肉は縮んで、背中の筋肉は伸びっぱなしになります。")
            article.append("この状態が続くと、体はその姿勢を「正常」だと思い込んでしまうんです。")
            article.append("")
            article.append("つまり、姿勢の問題って、実は筋肉のバランスの問題なんです。")
        elif 'プロテイン' in topic:
            article.append("そもそも、なぜプロテイン選びが難しいのか。")
            article.append("それは「何のために飲むのか」が曖昧だからなんです。")
            article.append("")
            article.append("筋肉をつけたいのか、食事の栄養バランスを整えたいのか、それとも単純にタンパク質が足りないのか。")
            article.append("目的によって、選ぶべきプロテインは全然違います。")
        elif '筋トレ' in topic:
            article.append("そもそも、なぜ筋トレが続かないのか。")
            article.append("多くの場合、それは「完璧を求めすぎるから」なんです。")
            article.append("")
            article.append("毎日やらないといけない、と思うから挫折する。")
            article.append("でも実際は、週2回でも十分効果は出るんです。")
        
        # とはいえ（けんすう式転換）
        article.append("")
        article.append("## とはいえ、○○だけの話でもない")
        article.append("")
        
        if '姿勢' in topic:
            article.append("「じゃあ筋トレすればいいのか」と思うかもしれませんが、それも半分正解で半分間違いです。")
            article.append("")
            article.append("確かに筋力は大切です。")
            article.append("でも、それ以上に大切なのが「日常の動作パターン」なんですよね。")
            article.append("")
            article.append("どんなに筋トレを頑張っても、1日8時間のデスクワークで前かがみになっていたら、その影響の方が大きいんです。")
            article.append("これ、ちょっと考えてみると当たり前の話ですよね。")
        elif 'プロテイン' in topic:
            article.append("「じゃあ食事から摂ればいいのか」と思うかもしれませんが、それも現実的には難しい場合があります。")
            article.append("")
            article.append("確かに食事からタンパク質を摂るのが理想です。")
            article.append("でも、毎日肉や魚を十分な量食べるのって、意外と大変なんですよね。")
        elif '筋トレ' in topic:
            article.append("「じゃあ週2回だけやればいいのか」と思うかもしれませんが、それも少し違います。")
            article.append("")
            article.append("確かに頻度は週2回でも大丈夫です。")
            article.append("でも、それよりも大切なのが「楽しく続けられるかどうか」なんですよね。")
        
        # 石原トレーナーの考え・提案
        article.append("")
        article.append("## 私が考える、もう少し楽なアプローチ")
        article.append("")
        article.append("というわけで、僕がお客様にお伝えしているアプローチは、こんな感じです。")
        article.append("")
        
        if '姿勢' in topic:
            article.append("まず「完璧な姿勢」を目指すのをやめること。")
            article.append("代わりに「今より少し楽になる姿勢」を見つけることから始めます。")
            article.append("")
            article.append("具体的には、デスクの高さやモニターの位置を調整する。")
            article.append("椅子を変える。")
            article.append("1時間に1回は立ち上がる習慣をつける。")
            article.append("こういう小さな変化から始めるんです。")
        elif 'プロテイン' in topic:
            article.append("まず「プロテインありき」で考えるのをやめること。")
            article.append("代わりに「今の食事で足りないタンパク質を補う」という考え方から始めます。")
            article.append("")
            article.append("具体的には、現在の食事でどのくらいタンパク質が摂れているかを確認する。")
            article.append("足りない分だけプロテインで補う。")
            article.append("続けやすい味や価格のものを選ぶ。")
            article.append("こんな感じで現実的に考えるんです。")
        elif '筋トレ' in topic:
            article.append("まず「毎日やらないといけない」という思い込みをやめること。")
            article.append("代わりに「週1回でもいいから続ける」ことから始めます。")
            article.append("")
            article.append("具体的には、楽しめる種目を見つける。")
            article.append("短時間でもいいから習慣にする。")
            article.append("結果より継続を重視する。")
            article.append("こういう考え方で取り組むんです。")
        
        # 実践的なアドバイス
        article.append("")
        article.append("そして、ストレッチやエクササイズは「○○を正す」ためではなく「体を動かしやすくする」ために行います。")
        article.append("硬くなった筋肉をほぐして、使えていない筋肉を動かす。")
        article.append("それだけで、自然と楽な状態が変わってくるんです。")
        
        # 気持ちの持ち方
        article.append("")
        article.append("## 気持ちの持ち方も大切")
        article.append("")
        article.append("最後に、これは僕の個人的な考えなんですが、一番大切なのは「自分を責めないこと」だと思っています。")
        article.append("")
        
        if '姿勢' in topic:
            article.append("「また猫背になってる」って気づいた時に、自分を責める必要はありません。")
            article.append("むしろ「気づけた自分、えらい！」って思ってもらいたいんです。")
        elif 'プロテイン' in topic:
            article.append("「今日もプロテイン飲み忘れた」って時に、自分を責める必要はありません。")
            article.append("むしろ「明日から気をつけよう」って思ってもらいたいんです。")
        elif '筋トレ' in topic:
            article.append("「今週も筋トレできなかった」って時に、自分を責める必要はありません。")
            article.append("むしろ「来週は1回でもやってみよう」って思ってもらいたいんです。")
        
        article.append("")
        article.append("気づくことができれば、少しずつ変えていくことができます。")
        
        # ゆるやかなまとめ（けんすう式）
        article.append("")
        article.append("## というわけで")
        article.append("")
        
        if '姿勢' in topic:
            article.append("姿勢改善は「背筋を伸ばす」ことではなく「体が楽になる環境を作ること」から始めてみてください。")
        elif 'プロテイン' in topic:
            article.append("プロテイン選びは「有名な商品を買う」ことではなく「自分に必要な分を見極めること」から始めてみてください。")
        elif '筋トレ' in topic:
            article.append("筋トレは「毎日やる」ことではなく「楽しく続けられる方法を見つけること」から始めてみてください。")
        else:
            article.append(f"{topic}は「完璧にやる」ことではなく「続けやすい方法を見つけること」から始めてみてください。")
        
        article.append("")
        article.append("完璧を目指さず、今より少しだけ楽になることを目標にする。")
        article.append("")
        article.append("そんな気持ちで取り組んでもらえたら、きっと続けやすいし、結果的に良い変化が生まれると思います。")
        
        return "\n".join(article)
    
    def extract_title_from_thought(self, thought):
        """考えからタイトルを抽出"""
        # 簡単なタイトル生成ロジック
        if 'プロテイン' in thought:
            if '継続' in thought or '続け' in thought:
                return "継続しやすさを重視"
            elif '必要' in thought:
                return "本当に必要かを考える"
            else:
                return "プロテインとの付き合い方"
        elif '筋トレ' in thought or 'トレーニング' in thought:
            if '週' in thought or '頻度' in thought:
                return "適切な頻度を見つける"
            elif '楽しく' in thought or '継続' in thought:
                return "楽しく続ける工夫"
            else:
                return "効果的なトレーニング"
        elif '姿勢' in thought or '猫背' in thought:
            if '根本' in thought:
                return "根本的な解決を目指す"
            elif '日常' in thought:
                return "日常生活の見直し"
            else:
                return "姿勢改善のコツ"
        else:
            return "大切なポイント"
    
    def clean_raw_thought(self, thought):
        """メモの断片を意味のある文章に変換"""
        # 関西弁の語尾「やな」を標準語に変換
        thought = re.sub(r'やな$', 'ですね', thought)
        thought = re.sub(r'やと', 'だと', thought)
        thought = re.sub(r'かな$', 'でしょうか', thought)
        thought = re.sub(r'やし', 'し', thought)
        thought = re.sub(r'へん', 'ない', thought)
        
        # 断片的なメモを完全な文章に変換
        conversions = {
            "お客様から「プロテイン美味しくて続けられる」と言われた": 
                "プロテインは美味しさと継続しやすさが重要だということを、お客様の声から実感しています。",
            "やっぱりプロテインは必要だと思います": 
                "適切なタンパク質摂取のために、プロテインは必要な栄養補助だと考えています。",
            "筋トレ頻度について質問された": 
                "筋トレの頻度については、週2回程度でも十分な効果が期待できると考えています。",
            "毎日やらなくても週2回で十分って伝えた": 
                "毎日トレーニングしなくても、週2回の継続的な実践で十分な効果が得られます。",
            "継続が一番大事": 
                "何よりも大切なのは、無理のない範囲で継続することです。",
            "お客様が「楽しくなってきた」って言ってくれた": 
                "トレーニングを楽しいと感じていただけることが、継続の秘訣だと実感しています。",
            "楽しさが継続の秘訣だと改めて実感": 
                "楽しく取り組めることが、長期継続の最も重要な要素だと考えています。",
            "反り腰の改善について相談された": 
                "反り腰の改善には、股関節の可動域向上など根本的なアプローチが必要です。",
            "よくある「背筋を伸ばしましょう」じゃ根本解決にならない": 
                "「背筋を伸ばす」だけでは表面的な対処に留まり、根本的な解決には至りません。",
            "股関節の可動域から見直しが必要": 
                "姿勢改善には、股関節の可動域など体の土台から見直すことが重要です。",
            "猫背改善のエクササイズを教えた": 
                "猫背改善には適切なエクササイズが有効ですが、日常の姿勢習慣も重要です。",
            "でも根本は座り方とか日常の姿勢": 
                "エクササイズも大切ですが、根本的には日常の座り方や立ち方を見直すことが重要です。",
            "エクササイズだけじゃ限界がある": 
                "エクササイズだけでなく、日常生活の姿勢習慣を見直すことが根本的な改善につながります。",
            "プロテインパウダーが苦手なお客様": 
                "プロテインパウダーが苦手な方には、食事からのタンパク質摂取をお勧めしています。",
            "食事から摂取する方法も提案した": 
                "サプリメントに頼らず、普段の食事からタンパク質を摂取する方法も有効です。",
            "無理にサプリに頼らなくてもいい": 
                "サプリメントありきではなく、まずは食事からの栄養摂取を基本に考えています。"
        }
        
        # 完全一致する変換があれば使用
        if thought in conversions:
            return conversions[thought]
        
        # 部分的な変換処理
        for key, value in conversions.items():
            if key in thought:
                return value
        
        # 語尾調整
        if not thought.endswith(('。', '！', '？', 'です', 'ます', 'でしょう')):
            if 'だと思う' in thought or '考え' in thought:
                thought += "と考えています。"
            elif '必要' in thought or '大切' in thought:
                thought += "だと思います。"
            else:
                thought += "。"
        
        return thought
    
    def expand_thought_for_note(self, thought):
        """note用に考えを詳しく展開"""
        # メモの断片的な部分を削除し、意味のある内容に変換
        clean_thought = self.clean_raw_thought(thought)
        
        expanded = []
        expanded.append(clean_thought)
        expanded.append("")
        expanded.append("私の経験では、画一的なアプローチではなく、")
        expanded.append("一人ひとりの体の特徴や生活習慣に合わせた方法が")
        expanded.append("最も効果的だと感じています。")
        expanded.append("")
        expanded.append("実際のセッションでも、この考えを基に")
        expanded.append("お客様それぞれに最適なアプローチを提案させていただいています。")
        
        return "\n".join(expanded)
    
    def expand_thought_for_ameblo(self, thought):
        """ameblo用に考えをカジュアルに展開"""
        # メモの断片的な部分を削除し、意味のある内容に変換
        clean_thought = self.clean_raw_thought(thought)
        
        expanded = []
        expanded.append(clean_thought)
        expanded.append("")
        expanded.append("って思うんです。")
        expanded.append("実際にお客様と関わってて感じることですし、")
        expanded.append("みんながみんな同じ方法で上手くいくわけじゃないですもんね💦")
        
        return "\n".join(expanded)
    
    def save_article(self, content, topic, platform):
        """記事をファイルに保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_topic = re.sub(r'[^\w\s-]', '', topic).strip()
        safe_topic = re.sub(r'[\s]+', '_', safe_topic)
        
        filename = f"{safe_topic}_{timestamp}.md"
        platform_dir = os.path.join(self.output_dir, platform)
        
        if not os.path.exists(platform_dir):
            os.makedirs(platform_dir)
        
        filepath = os.path.join(platform_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath, len(content)
    
    def generate(self, topic, platform):
        """記事生成のメイン処理"""
        if platform not in ['note', 'ameblo', 'blog']:
            print("エラー: プラットフォームは 'note', 'ameblo', または 'blog' を指定してください")
            return
        
        print(f"{platform}用の記事「{topic}」を生成中...")
        
        # スタイルガイドと現在の考えを読み込み
        style_guide = self.load_style_guide()
        current_thoughts = self.load_current_thoughts()
        
        # テーマに関連する考えを抽出
        relevant_thoughts = self.extract_relevant_thoughts(topic, current_thoughts)
        
        # プラットフォーム別に記事生成
        if platform == 'note':
            content = self.generate_note_article(topic, relevant_thoughts)
        elif platform == 'ameblo':
            content = self.generate_ameblo_article(topic, relevant_thoughts)
        elif platform == 'blog':
            content = self.generate_kensuu_style_blog(topic, relevant_thoughts)
        else:
            print(f"エラー: 不明なプラットフォーム '{platform}'")
            return
        
        # 保存
        filepath, char_count = self.save_article(content, topic, platform)
        
        print(f"記事を生成しました: {filepath}")
        print(f"文字数: {char_count}文字")
        print("石原トレーナーらしさ: 反映済み")
        if relevant_thoughts:
            print("最新の考え: 反映済み")
        else:
            print("最新の考え: デフォルトアドバイスを使用")

def main():
    if len(sys.argv) < 3:
        print("使用方法: python generate.py <テーマ> <プラットフォーム>")
        print("例: python generate.py \"プロテインの選び方\" note")
        print("例: python generate.py \"筋トレ継続のコツ\" ameblo")
        print("例: python generate.py \"姿勢改善の考え方\" blog")
        sys.exit(1)
    
    topic = sys.argv[1]
    platform = sys.argv[2]
    
    generator = IshiharaArticleGenerator()
    generator.generate(topic, platform)

if __name__ == "__main__":
    main()