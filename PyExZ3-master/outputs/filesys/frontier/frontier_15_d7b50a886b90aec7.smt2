(set-logic ALL)
; Constraint ID: d7b50a886b90aec7
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59407)) (False)
(assert (not (= x 59407)))

; Query: ((== x 59408)) (False)
(assert (not (not (= x 59408))))

(check-sat)
(get-model)
