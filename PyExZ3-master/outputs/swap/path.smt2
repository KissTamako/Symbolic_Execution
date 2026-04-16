(set-logic ALL)
; Executed Path ID: a71e203a4a1bb14c
; Generated at: 2026-04-17 03:12:56
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)

; ((> in1 in2)) (True)
(assert (> in1 in2))
; ((> (^ (^ in1 in2) (^ (^ in1 in2) in2)) (^ (^ in1 in2) in2))) (False)
(assert (not (> (^ (^ in1 in2) (^ (^ in1 in2) in2)) (^ (^ in1 in2) in2))))

(check-sat)
(get-model)
