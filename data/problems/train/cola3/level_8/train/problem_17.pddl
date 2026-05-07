

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b10)
(on b4 b6)
(on b5 b2)
(on b6 b5)
(on b7 b1)
(ontable b8)
(on b9 b7)
(on b10 b9)
(clear b3)
(clear b8)
)
(:goal
(and
(on b1 b4)
(on b3 b1)
(on b4 b2)
(on b5 b7)
(on b6 b3)
(on b8 b5)
(on b9 b10)
(on b10 b8))
)
)


