

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b10)
(on b3 b4)
(on b4 b7)
(on-table b5)
(on-table b6)
(on b7 b2)
(on b8 b9)
(on-table b9)
(on b10 b5)
(clear b1)
(clear b3)
(clear b6)
(clear b8)
)
(:goal
(and
(on b2 b8)
(on b3 b2)
(on b4 b1)
(on b5 b10)
(on b6 b7)
(on b8 b4)
(on b9 b3))
)
)


