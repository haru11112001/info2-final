import pyxel
import random

class PancakeGame:
    def __init__(self):
        # Pyxelの初期化
        pyxel.init(160, 120)
        pyxel.load("pancake_game_w.pyxres")

        # プレイヤーの初期位置とお皿の位置の設定
        self.player_x = 80
        self.plate_y = 110

        # パンケーキとワッフルのリスト、スコア、ゲームオーバーとゲームクリアの状態を管理する変数の初期化
        self.pan_cakes = []
        self.waffles = []  
        self.score = 0
        self.game_over = False
        self.game_clear = False
        self.game_clear_counter = 0
        
        # BGMの再生開始
        pyxel.play(0, 0, loop=True)

        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_over:  # ゲームオーバー状態でない場合にのみ更新する
            # 左右のキーに応じてプレイヤーの位置を移動
            if pyxel.btn(pyxel.KEY_LEFT):
                self.player_x = max(self.player_x - 2, 0)

            if pyxel.btn(pyxel.KEY_RIGHT):
                self.player_x = min(self.player_x + 2, 160 - 16)

            # 20フレームごとに新しいパンケーキとワッフルを生成
            if pyxel.frame_count % 20 == 0:
                pancake = {
                    "x": random.randint(0, 160 - 8),
                    "y": 0,
                    "falling": True,
                    "on_plate": False
                }
                self.pan_cakes.append(pancake)

                waffle = {
                    "x": random.randint(0, 160 - 8),
                    "y": 0,
                    "falling": True,
                    "on_plate": False
                }
                self.waffles.append(waffle)

            # ゲームクリア状態の場合、カウンターを増やして一定時間後にゲーム終了
            if self.game_clear:
                self.game_clear_counter += 1
                if self.game_clear_counter >= 10:
                    pyxel.quit()

            # パンケーキの移動と衝突判定
            for pancake in self.pan_cakes:
                if pancake["falling"]:
                    pancake["y"] += 2
                    if (
                        pancake["y"] + 8 >= self.plate_y and
                        self.player_x <= pancake["x"] <= self.player_x + 16
                    ):
                        pancake["falling"] = False
                        self.score += 1
                        pancake["on_plate"] = True

            # ワッフルの移動と衝突判定
            for waffle in self.waffles:
                if waffle["falling"]:
                    waffle["y"] += 2
                    if (
                        waffle["y"] + 8 >= self.plate_y and
                        self.player_x <= waffle["x"] <= self.player_x + 16
                    ):
                        waffle["falling"] = False
                        self.game_over = True  # ワッフルを取るとゲームオーバーになる
                        pyxel.stop(0)  # BGMの停止

            # 画面外に出たパンケーキとワッフルを削除
            self.pan_cakes = [pancake for pancake in self.pan_cakes if pancake["y"] < 120]
            self.waffles = [waffle for waffle in self.waffles if waffle["y"] < 120]
            
        # ゲームオーバー状態の場合、Qキーが押されたら終了
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

    def draw(self):
        # 画面のクリア
        pyxel.cls(15)
        
        # プレイヤーの描画
        pyxel.blt(self.player_x, self.plate_y, 0, 0, 0, 16, 8, 0)

        # パンケーキの描画
        for i, pancake in enumerate(self.pan_cakes):
            if pancake["falling"]:
                pyxel.blt(pancake["x"], pancake["y"], 0, 16, 0, 8, 8, 0)
            elif pancake["on_plate"]:
                stacked_y = self.plate_y - (i * 8)
                pyxel.blt(self.player_x + 4, stacked_y, 0, 24, 0, 8, 8, 0)
                if i == len(self.pan_cakes) - 1:
                    pyxel.blt(self.player_x + 4, stacked_y - 8, 0, 24, 0, 8, 8, 0)

        # ワッフルの描画
        for waffle in self.waffles:
            if waffle["falling"]:
                pyxel.blt(waffle["x"], waffle["y"], 0, 32, 0, 8, 8, 0)

        # スコアの表示
        pyxel.text(5, 5, f"Score: {self.score}", 7)

        # ゲームクリア状態の場合、ゲームクリアメッセージを表示
        if self.score >= 10:
            pyxel.cls(0)
            pyxel.text(60, 50, "GAME CLEAR", (pyxel.frame_count // 2) % 16)
            pyxel.text(60, 80, "Press [Q] to Quit", (pyxel.frame_count // 2) % 16)

        # ゲームオーバー状態の場合、ゲームオーバーメッセージを表示
        elif self.game_over:
            pyxel.cls(8)  # 画面を灰色で塗りつぶす
            pyxel.text(55, 50, "GAME OVER", 7)
            pyxel.text(50, 70, "Press [Q] to Quit", 7)

# ゲームの開始
PancakeGame()
