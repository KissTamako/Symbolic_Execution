(set-logic ALL)
; Constraint ID: 5ac4aa5ed9f93351
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60322)) (False)
(assert (not (= x 60322)))

; Query: ((== x 60323)) (False)
(assert (not (not (= x 60323))))

(check-sat)
(get-model)
