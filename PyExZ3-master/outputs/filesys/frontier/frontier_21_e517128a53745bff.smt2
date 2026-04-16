(set-logic ALL)
; Constraint ID: e517128a53745bff
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60391)) (False)
(assert (not (= x 60391)))

; Query: ((== x 60392)) (False)
(assert (not (not (= x 60392))))

(check-sat)
(get-model)
