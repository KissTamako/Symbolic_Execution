(set-logic ALL)
; Constraint ID: 90515a409de0d68d
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60094)) (False)
(assert (not (= x 60094)))

; Query: ((== x 60095)) (False)
(assert (not (not (= x 60095))))

(check-sat)
(get-model)
