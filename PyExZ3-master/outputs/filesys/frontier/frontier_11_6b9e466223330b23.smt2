(set-logic ALL)
; Constraint ID: 6b9e466223330b23
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59626)) (False)
(assert (not (= x 59626)))

; Query: ((== x 59627)) (False)
(assert (not (not (= x 59627))))

(check-sat)
(get-model)
