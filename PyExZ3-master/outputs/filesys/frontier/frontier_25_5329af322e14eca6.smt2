(set-logic ALL)
; Constraint ID: 5329af322e14eca6
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60697)) (False)
(assert (not (= x 60697)))

; Query: ((== x 60698)) (False)
(assert (not (not (= x 60698))))

(check-sat)
(get-model)
