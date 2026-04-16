(set-logic ALL)
; Constraint ID: 4dbcff898ceb28db
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60373)) (False)
(assert (not (= x 60373)))

; Query: ((== x 60374)) (False)
(assert (not (not (= x 60374))))

(check-sat)
(get-model)
