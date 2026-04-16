(set-logic ALL)
; Constraint ID: 66a2cb5823a6abc4
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59317)) (False)
(assert (not (= x 59317)))

; Query: ((== x 59318)) (False)
(assert (not (not (= x 59318))))

(check-sat)
(get-model)
