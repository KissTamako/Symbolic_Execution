(set-logic ALL)
; Executed Path ID: 1026a4db88845524
; Generated at: 2026-04-16 16:02:59
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)

; ((== (& in1 in2) 1)) (True)
(assert (= (& in1 in2) 1))
; ((== (& in1 in2) 7)) (False)
(assert (not (= (& in1 in2) 7)))

(check-sat)
(get-model)
