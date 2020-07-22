# Death Note

`heap`

## Code analysis

가장 큰 문제 : minus indexing이 가능함 -> got overwrite 가능(add) / libc leak도 가능(show)

read_input 함수는 null로 끝나지 않을 수 있음

is_printable은 중간에 null 넣으면 우회가능