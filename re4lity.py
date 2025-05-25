from manim import *

class Re4lityFadeIn(Scene):
    def construct(self):
        # 近未来的な紫のグラデーション色を定義
        neon_purple = "#8B00FF"
        electric_purple = "#6A0DAD"
        cyber_purple = "#9932CC"
        light_purple = "#DA70D6"
        
        # 背景を黒に設定
        self.camera.background_color = BLACK
        
        # テキストを作成（大きくて太いフォント）
        text = Text(
            "re4lity",
            font_size=72,
            font="Arial",
            weight=BOLD
        )
        text.move_to(ORIGIN)
        
        # 文字の輪郭のみのバージョンを作成
        outline_text = text.copy()
        outline_text.set_fill(opacity=0)  # 塗りつぶしを透明に
        outline_text.set_stroke(color=neon_purple, width=3, opacity=0)  # 輪郭を紫に
        
        # 塗りつぶし版を作成（グラデーション効果）
        filled_text = text.copy()
        filled_text.set_fill(color=[electric_purple, cyber_purple, light_purple], opacity=0)
        filled_text.set_stroke(color=neon_purple, width=2, opacity=0)
        
        # グロー効果用のテキスト（背景の光る効果）
        glow_text = text.copy()
        glow_text.set_fill(opacity=0)
        glow_text.set_stroke(color=light_purple, width=8, opacity=0)
        
        # 全てのテキストをシーンに追加
        self.add(glow_text, filled_text, outline_text)
        
        # アニメーション開始
        # 各文字を個別にアニメーション
        animations = []
        
        for i, char in enumerate("re4lity"):
            # 遅延を追加して左から右へのエフェクトを作成
            delay = i * 0.15
            
            # 輪郭のフェードイン
            outline_fadein = outline_text[i].animate.set_stroke(opacity=1)
            outline_fadein.run_time = 0.8
            
            # グロー効果のフェードイン
            glow_fadein = glow_text[i].animate.set_stroke(opacity=0.3)
            glow_fadein.run_time = 1.2
            
            # 塗りつぶしのフェードイン（輪郭の後に開始）
            fill_fadein = filled_text[i].animate.set_fill(opacity=0.9).set_stroke(opacity=0.8)
            fill_fadein.run_time = 1.0
            
            # アニメーションをタイムラインに追加
            animations.extend([
                AnimationGroup(
                    outline_fadein,
                    glow_fadein,
                    lag_ratio=0.2
                ),
                fill_fadein
            ])
        
        # 左から右へ段階的にアニメーション実行
        for i in range(len("re4lity")):
            delay = i * 0.2
            
            # 各文字のアニメーション
            self.play(
                outline_text[i].animate.set_stroke(opacity=1),
                glow_text[i].animate.set_stroke(opacity=0.3),
                run_time=0.6
            )
            
            # 少し遅れて塗りつぶし
            self.play(
                filled_text[i].animate.set_fill(opacity=0.9).set_stroke(opacity=0.8),
                run_time=0.8
            )
            
            # 短い間隔
            self.wait(0.1)
        
        # 最終的な光る効果
        self.play(
            glow_text.animate.set_stroke(opacity=0.5),
            run_time=0.5
        )
        
        # パルス効果（オプション）
        for _ in range(2):
            self.play(
                glow_text.animate.set_stroke(opacity=0.7),
                run_time=0.3
            )
            self.play(
                glow_text.animate.set_stroke(opacity=0.3),
                run_time=0.3
            )
        
        # 最後に少し待機
        self.wait(2)


# より高度なバージョン（パーティクル効果付き）
class Re4lityAdvanced(Scene):
    def construct(self):
        # 色定義
        neon_purple = "#8B00FF"
        electric_purple = "#6A0DAD"
        cyber_purple = "#9932CC"
        light_purple = "#DA70D6"
        
        self.camera.background_color = BLACK
        
        # メインテキスト
        text = Text(
            "re4lity",
            font_size=84,
            font="Arial",
            weight=BOLD
        )
        text.move_to(ORIGIN)
        
        # 複数レイヤーのテキスト作成
        # 1. 背景グロー（大きな光）
        bg_glow = text.copy()
        bg_glow.set_fill(opacity=0)
        bg_glow.set_stroke(color=light_purple, width=15, opacity=0)
        
        # 2. ミドルグロー
        mid_glow = text.copy()
        mid_glow.set_fill(opacity=0)
        mid_glow.set_stroke(color=cyber_purple, width=8, opacity=0)
        
        # 3. 輪郭
        outline = text.copy()
        outline.set_fill(opacity=0)
        outline.set_stroke(color=neon_purple, width=3, opacity=0)
        
        # 4. 塗りつぶし
        filled = text.copy()
        filled.set_fill(color=[electric_purple, neon_purple], opacity=0)
        filled.set_stroke(color=neon_purple, width=1, opacity=0)
        
        # シーンに追加
        self.add(bg_glow, mid_glow, outline, filled)
        
        # 左から右へのアニメーション
        for i in range(len("re4lity")):
            # 各文字の位置を取得
            char_center = text[i].get_center()
            
            # スパーク効果用の小さなドット
            sparks = VGroup()
            for _ in range(8):
                spark = Dot(
                    point=char_center + np.random.uniform(-0.5, 0.5, 3),
                    radius=0.02,
                    color=light_purple
                )
                sparks.add(spark)
            
            # アニメーション実行
            self.play(
                # グロー効果
                bg_glow[i].animate.set_stroke(opacity=0.2),
                mid_glow[i].animate.set_stroke(opacity=0.4),
                # 輪郭出現
                outline[i].animate.set_stroke(opacity=1.0),
                # スパーク出現
                *[spark.animate.set_opacity(1) for spark in sparks],
                run_time=0.5
            )
            
            # 塗りつぶしとスパーク消失
            self.play(
                filled[i].animate.set_fill(opacity=0.85).set_stroke(opacity=0.9),
                *[spark.animate.set_opacity(0) for spark in sparks],
                run_time=0.7
            )
            
            # スパークを削除
            self.remove(*sparks)
            
            self.wait(0.05)
        
        # 最終パルス効果
        self.play(
            bg_glow.animate.set_stroke(opacity=0.4),
            mid_glow.animate.set_stroke(opacity=0.6),
            run_time=0.3
        )
        self.play(
            bg_glow.animate.set_stroke(opacity=0.2),
            mid_glow.animate.set_stroke(opacity=0.4),
            run_time=0.5
        )
        
        self.wait(2)


# 使用方法:
# manim -pql scene.py Re4lityFadeIn
# または高度なバージョン:
# manim -pql scene.py Re4lityAdvanced