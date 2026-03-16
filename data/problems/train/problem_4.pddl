

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(ontable b3)
(on b4 b10)
(on b5 b12)
(on b6 b7)
(on b7 b3)
(on b8 b2)
(on b9 b5)
(ontable b10)
(on b11 b4)
(on b12 b6)
(clear b1)
(clear b8)
(clear b9)
(clear b11)
)
(:goal
(and
(on b2 b7)
(on b3 b6)
(on b5 b9)
(on b8 b10)
(on b10 b5)
(on b11 b3)
(on b12 b1))
)
)


