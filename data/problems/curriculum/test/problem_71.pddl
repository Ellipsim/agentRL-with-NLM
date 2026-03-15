

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on-table b1)
(on b2 b3)
(on-table b3)
(on-table b4)
(on-table b5)
(on b6 b4)
(on b7 b6)
(clear b1)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b3 b1)
(on b4 b5)
(on b5 b2)
(on b6 b3))
)
)


