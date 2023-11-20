import os
import re


# キャラの表情を格納するクラス
class CharaData:
    # コンストラクタ
    def __init__(self, name: str):
        self.name = name
        self.facial_expressions = []  # 表情差分の名前を格納するリスト

    # 表情差分を登録する
    def set_facial_expressions(self, face: str):
        self.facial_expressions.append(face)

    # 名前を取得
    def get_name(self):
        return self.name

    # 表情があるか確認する
    def exist_face(self, face: str):
        return face in self.facial_expressions


# キャラと表情を格納するクラス
class CharaDataList:
    # コンストラクタ
    def __init__(self):
        self.data_list = []  # CharaData を格納するリスト

    # キャラデータを登録する
    def set_chara(self, name: str, face: str):
        # name_dict にまだ登録されていなかったら登録する
        if not self.exist_chara(name):
            self.data_list.append(CharaData(name))

        self.data_list[self.locate_chara(name)].set_facial_expressions(face)

    # キャラクターがどこの配列に存在するか確認する
    def locate_chara(self, name: str):
        for index, data in enumerate(self.data_list):
            if name == data.get_name():
                return index

        return -1

    # キャラクターが存在するか確認
    def exist_chara(self, name: str):
        return self.locate_chara(name) != -1

    # キャラクターにその表情差分があるか確認する
    def exist_face(self, name: str, face: str):
        return self.data_list[self.locate_chara(name)].exist_face(face)


def load_file(input_string: str) -> str:
    while True:
        # ファイル名を入力
        file_name = input(input_string)

        # ファイル名からパスを作成
        file_path = "../scenario/" + file_name if file_name[-3:] == '.ks' else "../scenario/" + file_name + ".ks"

        # 拡張子がなければ付ける
        if file_path[-3:] != '.ks':
            file_path += ".ks"

        # ファイルの存在確認
        if not os.path.isfile(file_path):
            print("ファイル名が間違っています。")
            continue  # 見つからなかったらもう一度入力させる

        return file_path


# 行ごとのデバッグ
def confirm_bug(text: str):
    # 端の空白を削除
    text = text.strip()

    # その行に何も書いてなかったら弾く
    if not text:
        return

    # タグだけを見るので、始まりの括弧がなかったら弾く
    if not text[0] == "[":
        return

    # テキストを空白で分割する
    statements = text.split()

    # 括弧を削除
    statements[0] = statements[0][1:]
    statements[-1] = statements[-1][:-1]

    # タグを検索
    if statements[0] == "chara_mod":
        # パラメータの数が少ない -> エラー
        if len(statements) <= 2:
            output_error(row, "パラメータの数が足りません。")
            return

        # 1個目のパラメータが name= で始まってない -> タイプミス
        if len(statements[1]) <= 5 or not statements[1][:5] == "name=":
            output_error(row, "タイプミス 「name」")
            return

        # 1個目のパラメータが face= で始まってない -> タイプミス
        if len(statements[2]) <= 5 or not statements[2][:5] == "face=":
            output_error(row, "タイプミス 「face」")
            return

        # 名前と表情差分をそれぞれ取得
        name = statements[1][5:]
        face = statements[2][5:]

        # キャラクターが定義されているか確認
        if not chara_data_list.exist_chara(name):
            output_error(row, name + "は存在しないキャラクターです。")
            return

        # キャラクターに表情差分が定義されているか確認
        if not chara_data_list.exist_face(name, face):
            output_error(row, name + "に" + face + "の表情差分は存在しません。")

    elif statements[0] == "chara_show":
        # パラメータの数が少ない -> エラー
        if len(statements) <= 3:
            output_error(row, "パラメータの数が足りません。")
            return

        # 1個目のパラメータが name= で始まってない -> タイプミス
        if len(statements[1]) <= 5 or not statements[1][:5] == "name=":
            output_error(row, "タイプミス 「name」")
            return

        # 1個目のパラメータが face= で始まってない -> タイプミス
        if len(statements[2]) <= 5 or not statements[2][:5] == "face=":
            output_error(row, "タイプミス 「face」")
            return

        # 名前と表情差分をそれぞれ取得
        name = statements[1][5:]
        face = statements[2][5:]

        # キャラクターが定義されているか確認
        if not chara_data_list.exist_chara(name):
            output_error(row, name + "は存在しないキャラクターです。")
            return

        # キャラクターに表情差分が定義されているか確認
        if not chara_data_list.exist_face(name, face):
            output_error(row, name + "に" + face + "の表情差分は存在しません。")
            return


def output_error(row: int, text: str):
    print(str(row) + "行:" + text)


#  ------------------------------------------------------- #


chara_data_list = CharaDataList()

chara_path = load_file("キャラデータのファイル名を入力してください。: ")

with open(chara_path, 'r', encoding='UTF-8') as f:
    # キャラデータの文章を全て取得
    chara_data_code = f.read()

    # こんな感じで書いてたら (.?*) の所を取得しますよ。っていうルールを作る
    pattern = '\[chara_face name=(.*?) face=(.*?) storage='
    pattern2 = '\[chara_new name=(.*?) face=(.*?) storage='

    # 上で作ったルールを適用して名前と表情差分を全部抜き出す
    chara_data = re.findall(pattern, chara_data_code) + re.findall(pattern2, chara_data_code)

    # データを chara_data_list に追加
    for data in chara_data:
        chara_data_list.set_chara(data[0], data[1])

while True:
    # シナリオファイルを開く
    scenario_path = load_file("シナリオデータのファイル名を入力してください。: ")

    # ファイルを開く
    with open(scenario_path, 'r', encoding='UTF-8') as f:
        # ファイルを一行づつ読んでいく
        for row, text in enumerate(f, start=1):
            confirm_bug(text)

    is_continue = input("終了する場合はnと入力してください。")

    # nが入力されたらループを抜ける
    if is_continue == 'n':
        break
