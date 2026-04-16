(set-logic ALL)
; Constraint ID: 178fed47648d537f
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59242)) (False)
(assert (not (= x 59242)))

; Query: ((== x 59243)) (False)
(assert (not (not (= x 59243))))

(check-sat)
(get-model)
