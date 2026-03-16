

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(ontable b3)
(on b4 b8)
(ontable b5)
(on b6 b11)
(on b7 b1)
(on b8 b6)
(ontable b9)
(on b10 b12)
(on b11 b10)
(on b12 b3)
(clear b2)
(clear b4)
(clear b7)
(clear b9)
)
(:goal
(and
(on b3 b12)
(on b4 b7)
(on b5 b10)
(on b6 b9)
(on b7 b6)
(on b9 b8)
(on b10 b3)
(on b11 b5))
)
)


