(set-logic ALL)
; Path ID: c581b954ca54a498
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59386)) (False)
(assert (not (not (= x 59386))))

(check-sat)
(get-model)
