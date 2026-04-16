(set-logic ALL)
; Constraint ID: 8dec316113b6ccba
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59854)) (False)
(assert (not (not (= x 59854))))

(check-sat)
(get-model)
