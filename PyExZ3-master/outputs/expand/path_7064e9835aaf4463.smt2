(set-logic ALL)
; Executed Path ID: 7064e9835aaf4463
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)

; ((>= (+ in1 in2) 4294967296)) (True)
(assert (>= (+ in1 in2) 4294967296))

(check-sat)
(get-model)
