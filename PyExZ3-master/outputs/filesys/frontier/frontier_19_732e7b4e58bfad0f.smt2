(set-logic ALL)
; Constraint ID: 732e7b4e58bfad0f
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59863)) (False)
(assert (not (= x 59863)))

; Query: ((== x 59864)) (False)
(assert (not (not (= x 59864))))

(check-sat)
(get-model)
