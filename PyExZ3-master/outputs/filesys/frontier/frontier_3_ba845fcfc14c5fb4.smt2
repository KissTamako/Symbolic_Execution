(set-logic ALL)
; Constraint ID: ba845fcfc14c5fb4
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59314)) (False)
(assert (not (= x 59314)))

; Query: ((== x 59315)) (False)
(assert (not (not (= x 59315))))

(check-sat)
(get-model)
