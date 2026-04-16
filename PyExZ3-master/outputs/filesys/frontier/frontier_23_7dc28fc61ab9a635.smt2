(set-logic ALL)
; Constraint ID: 7dc28fc61ab9a635
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60694)) (False)
(assert (not (= x 60694)))

; Query: ((== x 60695)) (False)
(assert (not (not (= x 60695))))

(check-sat)
(get-model)
