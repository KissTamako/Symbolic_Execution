(set-logic ALL)
; Constraint ID: 6106ea45fc8e155a
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60148)) (False)
(assert (not (= x 60148)))

; Query: ((== x 60149)) (False)
(assert (not (not (= x 60149))))

(check-sat)
(get-model)
