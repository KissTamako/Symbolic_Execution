(set-logic ALL)
; Constraint ID: a2806099d1a020b3
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59323)) (False)
(assert (not (= x 59323)))

; Query: ((== x 59324)) (False)
(assert (not (not (= x 59324))))

(check-sat)
(get-model)
