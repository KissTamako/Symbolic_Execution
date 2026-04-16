(set-logic ALL)
; Executed Path ID: 919d0815ea9d3890
; Generated at: 2026-04-17 03:12:52
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const a Int)
(declare-const b Int)

; ((== a 1)) (True)
(assert (= a 1))
; ((== b 2)) (True)
(assert (= b 2))

(check-sat)
(get-model)
