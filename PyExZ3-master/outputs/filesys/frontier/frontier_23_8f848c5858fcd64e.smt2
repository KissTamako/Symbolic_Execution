(set-logic ALL)
; Frontier Constraint ID: 8f848c5858fcd64e
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 520)) (False)
(assert (not (= x 520)))

; Query: ((== x 521)) (False)
(assert (not (not (= x 521))))

(check-sat)
(get-model)
