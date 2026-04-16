(set-logic ALL)
; Path ID: 0f358f343d8f015e
; Generated at: 2026-04-16 12:01:19
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const a Int)
(declare-const se Int)

; ((== a 9223372036854775807)) (False)
(assert (not (= a 9223372036854775807)))

; Query: ((== a 9223372036854775808)) (True)
(assert (not (= a 9223372036854775808)))

(check-sat)
(get-model)
