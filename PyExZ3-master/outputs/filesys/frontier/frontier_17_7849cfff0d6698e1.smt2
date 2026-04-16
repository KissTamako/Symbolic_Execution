(set-logic ALL)
; Constraint ID: 7849cfff0d6698e1
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60160)) (False)
(assert (not (= x 60160)))

; Query: ((== x 60161)) (False)
(assert (not (not (= x 60161))))

(check-sat)
(get-model)
