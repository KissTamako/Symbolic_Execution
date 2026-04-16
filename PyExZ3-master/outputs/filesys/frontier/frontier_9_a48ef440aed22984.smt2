(set-logic ALL)
; Constraint ID: a48ef440aed22984
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60598)) (False)
(assert (not (= x 60598)))

; Query: ((== x 60599)) (False)
(assert (not (not (= x 60599))))

(check-sat)
(get-model)
