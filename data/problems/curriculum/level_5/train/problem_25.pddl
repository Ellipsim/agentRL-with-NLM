

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b7)
(on-table b2)
(on-table b3)
(on b4 b3)
(on-table b5)
(on b6 b1)
(on-table b7)
(clear b2)
(clear b4)
(clear b5)
(clear b6)
)
(:goal
(and
(on b3 b1)
(on b4 b6)
(on b6 b3)
(on b7 b4))
)
)


