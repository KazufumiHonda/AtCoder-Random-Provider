# AtCoder Random Problem Provider
## 概要
- discord bot
- AtCoderの問題を無作為に1問選んでくれるBot

## 仕様
- メンションすると、問題のURLを1つ返す
- 返す問題はABC,ARC,AGCの中から選ばれる
- 難易度選択
     - difficultyを数値で指定
          - @AtCoder Random Problem Provider 下限 上限
          - 下限・上限は数値で指定
          - デフォルト値の場合は def と指定
     - difficultyを色で指定
          - 灰diff:灰 または GRY
          - 茶diff:茶 または BRN
          - 緑diff:緑 または GRN
          - 水diff:水 または AQU
          - 青diff:青 または BLU
          - 黃diff:黃 または YEL
          - 赤diff:赤 または RED
          - 銀diff:銀 または SIL
          - 金diff:金 または GLD
     - 指定しない場合は全範囲から無作為に選択される
