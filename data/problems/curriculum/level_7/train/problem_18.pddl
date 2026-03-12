

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b3)
(on-table b3)
(on b4 b7)
(on-table b5)
(on b6 b4)
(on-table b7)
(on-table b8)
(clear b1)
(clear b2)
(clear b6)
(clear b8)
)
(:goal
(and
(on b4 b3)
(on b5 b8)
(on b7 b5))
)
)


