

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b7)
(on b3 b1)
(on b4 b5)
(on-table b5)
(on-table b6)
(on b7 b6)
(clear b2)
(clear b3)
)
(:goal
(and
(on b1 b5)
(on b4 b3)
(on b5 b7))
)
)


