(set-logic ALL)
; Executed Path ID: 9cbeb2fd67a78843
; Generated at: 2026-04-17 03:12:43
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const a Int)

; ((== a 9223372036854775807)) (False)
(assert (not (= a 9223372036854775807)))
; ((== a 9223372036854775808)) (True)
(assert (= a 9223372036854775808))

(check-sat)
(get-model)
