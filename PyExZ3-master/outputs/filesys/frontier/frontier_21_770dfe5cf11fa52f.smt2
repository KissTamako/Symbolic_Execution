(set-logic ALL)
; Constraint ID: 770dfe5cf11fa52f
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59491)) (False)
(assert (not (= x 59491)))

; Query: ((== x 59492)) (False)
(assert (not (not (= x 59492))))

(check-sat)
(get-model)
