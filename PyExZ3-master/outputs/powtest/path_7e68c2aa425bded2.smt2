(set-logic ALL)
; Executed Path ID: 7e68c2aa425bded2
; Generated at: 2026-04-16 16:03:02
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const in1 Int)

; ((== (* in1 in1) 0)) (False)
(assert (not (= (* in1 in1) 0)))
; ((> (* in1 in1) 0)) (True)
(assert (> (* in1 in1) 0))

(check-sat)
(get-model)
