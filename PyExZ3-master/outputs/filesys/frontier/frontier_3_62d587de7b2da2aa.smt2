(set-logic ALL)
; Constraint ID: 62d587de7b2da2aa
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60589)) (False)
(assert (not (= x 60589)))

; Query: ((== x 60590)) (False)
(assert (not (not (= x 60590))))

(check-sat)
(get-model)
