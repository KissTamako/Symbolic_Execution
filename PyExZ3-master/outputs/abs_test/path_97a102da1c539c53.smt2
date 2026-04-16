(set-logic ALL)
; Executed Path ID: 97a102da1c539c53
; Generated at: 2026-04-16 13:27:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const a Int)

; ((< a 0)) (False)
(assert (not (< a 0)))

(check-sat)
(get-model)
