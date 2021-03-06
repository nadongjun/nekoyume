# Nekoyume: 分散型大規模多人数同時参加型オンラインRPG

**概要:** Nekoyumeはブロックチェーンベースの分散型MMORPGです。多数のユーザーが仮想世界の中のモンスターを倒して経験を獲得したり、冒険の重要なアイテムを収集したりしてより強くなることができます。ゲームの行動情報をブロックチェーンに記録することで、ノード間の通信を介して中央サーバがなくても、多数のユーザーが参加できるゲームを構成しました。ゲームに必要なランダム要素をブロックチェーン上で実装できるためにハッシュランダムという別のランダムコンセンサスをデザインしました。ハッシュランダムは、プルーフ・オブ・ワーク(POW)によって作成され、ブロックハッシュと、個々の行動のハッシュ値を組み合わせて予測が難しく、特定の利害関係者の意図を最小限に抑え、個々の行動に決定的なランダムコンセンサスです。


## 1. 背景

サトシ・ナカモトが提案したビットコインは、従来の電子署名、ハッシュ、POWなどの技術を利用してブロックチェーンという概念を提示しました。ブロックチェーンは9年間のメインネットが安定的に動作し、脱集中されて誰でも参加可能な、信頼できる仮想通貨を作ることができていることを示しました。[<sup>1</sup>]ブロックチェーンは、ビットコインを作るために提案されたが、この技術が提示する誰でも参加可能な信頼システムというビジョンは、複数のソフトウェアプロジェクトに大きな影響を与えました。

今ブロックチェーンは貨幣以上に色々なところに活用されています。ヴィタリック・ブテリンは、ビットコインのスクリプトをさらに発展させ、チューリング完全なスマート・コントラクトをもとにした分散型アプリケーション・プラットフォームであるイーサリアムを提案しました。[<sup>2</sup>]イーサリアムの登場以来、ブロックチェーン上のマーケットプレイス、ソーシャルネットワークサービス、取引所など、さまざまなアプリケーションが作られ始めました。

ブロックチェーンでさまざまなアプリケーションを作成することができるようになると、ゲームを作成するための試みも出ました。特にランダムに生成された猫を送受信することができるクリプトキティ[<sup>3</sup>]は、イーサリアムネットワークが一時的に麻痺される現象まで見せ、熱狂的な反応を引き出しました。しかし、ブロックチェーン上でランダムの使用は非常に限定的であるため、現在実装することができるゲームも制約がありました。より汎用的なランダム方式が提案ならば、より多くの種類のゲームアプリケーションを開発することができます。


## 2. 擬似乱数生成（PRNG）

ブロックチェーンは、すべての元帳を共有する性質チェーン上のデータとその実行結果が決定的でなければならないという制約があります。つまり、ブロックチェーン上のアプリケーションで一般的なランダム値を活用すれば、同じデータに基づいて、すべての他の値を見ることができるので、これを根本的に禁止するしかありません。しかし、テトリスを含む多くの普及したゲームには、ランダム要素が存在して、ランダムなくブロックチェーン上でゲームを実装することは、大きな制約がありました。そのため、ブロックチェーンをより汎用的に使用できるようにするためにブロックチェーン上での擬似ランダム生成（PRNG）の研究がありました。


### 2.1. ブロック値を活用したランダム生成

ブロック内のアクセス可能な変数をシードとして利用してランダムに生成するための戦略が初めて提示されました。[<sup>4</sup>]この方法は、簡単にランダム実装が可能ですが、採掘者がすべてのブロックの変数を編集することができるのために、採掘者とユーザーが同一になることができるブロックチェーンに適した方法はありません。

### 2.2. 外部サービスを活用したランダム生成

外部サービスを介して現在の行動のランダム値を取得し、適用する方法もあります。[<sup>5</sup>]これは、ランダムに作成された方式を完全に非公開にすることができますが、分散された方法ではないので、外部サービスの信頼の問題が発生します。

このように、現在提案されているランダム生成方式は、特定の集団の意図介入が可能であるという短所があります。カジノでディーラーが確率を変造できないように、ランダムには、特定の利害関係の意図介入の可能性を最小化し、公正に作成する必要があります。この問題を解決するためにNekoyumeはハッシュランダムというランダム生成方式を提案します。

## 3. ハッシュランダム

ハッシュランダムはNekoyumeが提示するランダムコンセンサスです。ハッシュランダムは、利害関係者が意図的に有利な手を出すための試みを遮断したり、しようとしても利害関係上の損害が出るようにデザインしました。このため、二つの主要な概念を提示します。

### 3.1. 行動情報のハッシュとブロックハッシュの組み合わせ

ユーザーの行動情報の内容を利用して出てきたハッシュ値は、ユーザーの署名が含まれているため、採掘者が意図的に変形することができません。ブロックハッシュは採掘者が作成する値であるため、ユーザーが意図的に介入することはできません。 2つのハッシュ値をXORした値をランダムシードに活用し、（1）ユーザーがランダム値に介入することはできませんし、（2）ブロック内のすべてのユーザーの行動は、個々のランダムシードをもとに行われることがあります。

### 3.2. ブロックに含めることができる行動情報の時間制限

行動情報のハッシュとブロックハッシュの組み合わせをランダムシードとして活用しても採掘が意図的に自分と利害関係が合うユーザーの行動情報に基づいて有利なハッシュの生成を試みることができます。これを牽制するためには、ブロックに含まれることができる行動情報の時間は、最大ブロックの作成時間の10倍以内に制限します。採掘は、特定の行動情報との組み合わせが有利ハッシュを見つけるために、他の採掘者よりも多くの時間を投資することができますが、以下のような損害を受けます。

- 採掘者ハッシュ補償の競争で不利な位置になります。
- 行動情報が定期的に更新が必要するため、有利なブロックを意図的に探す過程は長くなります。

## 4. 分散されたMMORPG

Nekoyumeは、ハッシュランダムの概念を初めて適用したブロックチェーンベースのMMORPGです。参加者は、冒険家になって、ゲームの中の世界で冒険をしたり取引をしたりとか、猫になって、ゲームの進行に重要なブロック探索を行うこともできます。

NekoyumeはブロックチェーンベースのMMORPGであるため、特定の主体の中央サーバーが存在しません。これは以下のような利点を持ちます。

1. 特定の主体によって運営されている集中型サービスは、そのゲームの収益性によってサービスが継続的に運営されていない可能性があります。ブロックチェーンベースのゲームは、参加者が1人でも残っている場合、ゲームを続行することができます。

2. 運営主体の事業的な意図によってゲームの楽しさの要素が運営主体の収益性に合わせて大きく変更されることがありません。ゲーム性の変更は、参加者の中心のコミュニティの慎重な協議によって決定されるので、参加者の多くがしたいゲームの楽しさの要素を適切に育てていくことができます。

3. 集中型サービスは、サービス運営主体に経済的利益が集中しますが、ブロックチェーンベースのゲームは、合意されたトークンの経済モデルに合わせてゲームの補償が分配されます。

## 5. 経済構造

次はNekoyumeの猫参加者と冒険の参加者がお互いに共有している要素の簡単な図表です。

    +-----------+                 +--------------+
    |           | → Block, Gold → |              |
    |    Cat    |                 |  Adventurer  |
    |           | ← Move,  Item ← |              |
    +-----------+                 +--------------+

### 5.1. 冒険家

冒険は、自分の職業を設定し、冒険をしアイテムと経験を集めて成長し、より強くすることができます。以下のような行動を行うことができます。

##### 5.1.1 ⚔️接近戦

```
👶 ET8ngv ∙ 2018-04-16 15:43:44.290364

👍 戦闘勝利!

💥 Griffinに 2 ダメージを与えた。 (HP 10 → 8)
😫 Griffinに攻撃されて 8 ダメージを受けた
🤔 私はさっきの間違いで学びを得た。 (XP +1)
💥 Griffinに 2 ダメージを与えた。 (HP 8 → 6)
💥 Griffinに 1 ダメージを与えた。 (HP 6 → 5)
💥 Griffinに 2 ダメージを与えた。 (HP 5 → 3)
💥 Griffinに 1 ダメージを与えた。 (HP 3 → 2)
💥 Griffinに 4 ダメージを与えた。 (HP 2 → -2)
☠️ Griffinを打ち負かした!
🎁 CHKNを得た！
```

現在のセクションで出没するモンスターと戦闘を着ています。

##### 5.1.2. 睡眠

```
👶 ET8ngv ∙ 2018-04-16 23:43:47.534060

💤睡眠を介して体力回復
```

睡眠をとって体力を回復します。

##### 5.1.3 🆙レベルアップ

```
👶 J4tQdM ∙ 2018-04-16 23:45:50.855538

🆙レベルアップ！今レベル4です。
```

レベルを上げて能力値を向上させます。

行動を宣言すると、ネットワークに行動情報が伝達され、次のブロックが生成されるとき、実際に行動が行われます。ブロック生成周期は15秒であり、ブロックにしたユーザーの両方の行動が含まれることがないので、最小動作周期は15秒になります。

ブロックの作成が完了すると、そのブロックに含まれている行動が評価されます。評価時ハッシュランダムで決定されたランダム値が行動の結果に反映されるが、ハッシュランダムでランダム値が作られる過程は以下の通りです。

```python
>>> move.hash
'42ff1bb9d4149463474a9c84cb1f580e3d78176038646d7bd66b135fa34bc739'

>>> move.block.hash
'0000009d0d9bdd3fdfcd5a39d6313c6454653d881a3a59068c8a026ddf4f5803'

>>> randoms = [ord(a) ^ ord(b) for a, b in zip(move.block.hash, move.id)]
[4, 2, 86, 86, 1, 82, 91, 93, ... 3, 10]

>>> randoms = randoms[int(move.block.difficulty / 4):]
[1, 82, 91, 93, ... 3, 10]
```

冒険は冒険を通じて、さまざまなアイテムを獲得することができます。しかし、金は、取引を介してのみ獲得が可能なため、冒険を通じて成長してより強いモンスターとの戦いを通して良いアイテムを獲得する必要が市場で多くの金を受け取ることができます。

冒険のライフサイクルは、[ダンジョンワールド]規則を採択しました。ダンジョンワールドはSage LaTorraとAdam Koebelの「アポカリプスワールドエンジン」をベースに作成されたファンタジーTRPGルールです。ダンジョンワールドは、プレイヤーのやりとりが非常に重要なTRPGの特性を継承しているため、複数のユーザーを含むブロックチェーンのアプリケーションに適しています。また、六面体サイコロを2回転がすことにより、ユーザの行動の全てが判定されるようになっているため、ランダム要素の使用に適している。

### 5.2. 猫

猫はビットコインでの採掘者の役割と同じです。冒険の行動情報が入ってくると、他の猫に行動情報を共有し、行動情報をパッケージするブロックを移動します。

#### 5.2.1. ブロック生成コンセンサス

Nekoyumeは、ハッシュランダムを使用するために作業情報を主要コンセンサスで採択したので、プロトコルで提示する難易度に基づいて、ハッシュキャッシュを進める必要があります。ブロック生成周期は15秒を目標にしているので、最近ブロック生成時間の平均が15秒よりも低い場合に要求難易度は上がり、逆に15秒より高い要求難易度は低くなります。

#### 5.2.2. 報酬システム

ブロック探索が完了すると、採掘者報酬としてゴールドを受け取ることができます。ゴールドの報酬は、初期には、ブロックごとに16ゴールドが支給され、4年に一度の半減期を迎え、16年目からは、ブロックごとに1ゴールドで固定されるようになります。この補償は、クライアントと採掘者と1/2に分けて分配となるため、実質的に最初の年に猫が直接受ける報酬は、8ゴールドとなり、16年目からは、ブロックごとに0.5ゴールドを取得します。

```eval_rst
+-----------------------------------+-----------------------+
| クライアントと採掘者が受ける総合ゴールド/4y  | 　　ブロックごとのゴールド 　|
+===================================+=======================+
|                       134,553,600 |                    16 |
+-----------------------------------+-----------------------+
|                        67,276,800 |                     8 |
+-----------------------------------+-----------------------+
|                        33,638,400 |                     4 |
+-----------------------------------+-----------------------+
|                        16,819,200 |                     2 |
+-----------------------------------+-----------------------+
|                         8,409,600 |                     1 |
+-----------------------------------+-----------------------+
```

### 5.3 ゴールド

分散化されたコミュニティが持続可能するためには、生産と消費が合理的にバランスを達成することができます経済構造が必要です。ゴールドは、Nekoyumeの中心の仮想通貨であり、これを発行して交換し、消費者は、楽しいゲーム体験を、生産者は、貢献のための合理的な補償を受けることができます。

#### 5.3.1. ゴールド使用の利点

冒険は、ゴールドを使用して、より快適で高速なゲーム体験をすることができます。代表的には、下記のようなメリットが存在します。

- 🔼　保有量に比例した能力値ボーナス獲得
- 🤓　アイテム合成を通じた貴重品獲得
- 🤝　アイテムの取引を通じた様々なアイテムを収集

#### 5.3.2. ゴールドの獲得方法

#### 5.3.2.1 ゴールド発行イベント

開発初期の時点である2018年5月に、メインネットで使用できるNekoyumeゴールド（NYG）をイーサリアムERC20トークンの形で発行する予定です。総発行量の21％を活用する予定であり、これはメインネットランチング以後最初に使用できる方法です。この発行を通じ、二つの目的を達成します。

1. 有償販売：99％（20.79％）は、販売を進めて初期貢献を補償する開発資金を確保します。
2. 無償配布：1％（0.21％）は、初期のプレーヤーのコミュニティを拡張するためのマーケティングを進めています。

#### 5.3.2.2 コアチームに参加する

今後1年の集中開発期間のコアチームに参加される方々に予約されて9％のゴールドを貢献量に比例して分配する予定です。 1番と同様に、初期の集中開発のための補償方法です。

#### 5.3.2.3 ネットワークに参加する

メインネットランチング以降、公開されたコードを元にプレイヤーにクライアントを提供するか、猫を実行してブロックを作成すると、これに合わせて報酬を得ることができます。全体補償割合の中で最も大きな規模を占め、2019年からゴールドを得ることができる唯一の方法になる予定です。


## 6. 限界

ハッシュランダムブロックチェーンの上の利害関係者の関与を最小限にするランダムコンセンサスだが、以下のような制限があります。

### 6.1. ハッシュランダムの限界

ハッシュランダムは、ユーザーにランダムに介入する余地をなくして、採掘者には利害関係上、比較的ランダムな結果を意図していない作業証明が最も大きな利益になるようにランダム介入に制約を追加しました。しかし、もしゲームでランダムを通じて提示する利益が、この構造の損害を無視できるほど大きな報酬であれば、採掘者の制約を考慮し、意図的なハッシュの生成を試みることができます。したがって、ハッシュランダムを書くことも、ランダムに過度の補償がなされはないシステムを設計する必要があります。

### 6.2. POWの強制

ハッシュランダムは、POWと一緒に使われることを前提に設計されました。POS（プルーフ・オブ・ステーク）やその他のコンセンサス方式を使用する生態系であれば、採掘者が簡単にランダムに介入することができますので、ハッシュランダムの導入は適切ではありません。

## 7. 結論

Nekoyumeは分散型MMORPGを作るために既存のビットコイン、イーサリアムのコンセンサスシステムを持ってきて、ハッシュランダムという新しい方式のランダムコンセンサスを提案し、これを実装しました。このホワイトペーパーでは、既存のブロックチェーンのランダム生成方式とハッシュランダムの違いを整理し、それによってNekoyumeがどのような形で開発されているかどうかを一緒に見てみました。また、ハッシュランダムは、POWと一緒に使われなければならなく、ハッシュランダムを使ってもランダム値によるイベントで過度な報酬は与えないようにする必要があります。


[<sup>1</sup>]: https://bitcoin.org/bitcoin.pdf
[<sup>2</sup>]: https://github.com/ethereum/wiki/wiki/%5BKorean%5D-White-Paper
[<sup>3</sup>]: https://www.dropbox.com/s/a5h3zso545wuqkm/CryptoKitties_WhitePapurr_V2.pdf?dl=0
[<sup>4</sup>]: https://etherscan.io/address/0xa11e4ed59dc94e69612f3111942626ed513cb172#code
[<sup>5</sup>]: http://www.oraclize.it/
[ダンジョンワールド]: http://www.dungeon-world.com/