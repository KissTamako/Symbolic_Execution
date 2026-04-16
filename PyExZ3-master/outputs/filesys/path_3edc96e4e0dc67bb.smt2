(set-logic ALL)
; Executed Path ID: 3edc96e4e0dc67bb
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 448)) (False)
(assert (not (= x 448)))
; ((== x 449)) (False)
(assert (not (= x 449)))

(check-sat)
(get-model)
