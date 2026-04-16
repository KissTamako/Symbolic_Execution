(set-logic ALL)
; Constraint ID: e1b6c4a4beb63d0f
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59710)) (False)
(assert (not (= x 59710)))

; Query: ((== x 59711)) (False)
(assert (not (not (= x 59711))))

(check-sat)
(get-model)
