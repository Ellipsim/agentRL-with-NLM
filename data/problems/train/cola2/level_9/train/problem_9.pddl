

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b1)
(ontable b4)
(on b5 b9)
(on b6 b5)
(on b7 b4)
(ontable b8)
(on b9 b7)
(on b10 b8)
(clear b2)
(clear b3)
(clear b10)
)
(:goal
(and
(on b1 b7)
(on b2 b3)
(on b4 b10)
(on b5 b6)
(on b6 b9)
(on b7 b8)
(on b9 b2)
(on b10 b1))
)
)


