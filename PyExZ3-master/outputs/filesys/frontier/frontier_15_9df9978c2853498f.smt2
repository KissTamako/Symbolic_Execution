(set-logic ALL)
; Constraint ID: 9df9978c2853498f
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60007)) (False)
(assert (not (= x 60007)))

; Query: ((== x 60008)) (False)
(assert (not (not (= x 60008))))

(check-sat)
(get-model)
