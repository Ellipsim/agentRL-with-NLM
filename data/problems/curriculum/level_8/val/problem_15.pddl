

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b1)
(on-table b3)
(on-table b4)
(on b5 b2)
(on b6 b10)
(on-table b7)
(on-table b8)
(on b9 b8)
(on b10 b5)
(clear b3)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b5)
(on b3 b9)
(on b4 b7)
(on b5 b4)
(on b6 b3)
(on b9 b10)
(on b10 b1))
)
)


